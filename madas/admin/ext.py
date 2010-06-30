from django.conf.urls.defaults import patterns, url
from django.core.exceptions import FieldError
from django.db import transaction
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseNotFound, HttpResponseServerError
from django.utils.encoding import smart_str
from json import dumps, loads


class ExtJsonInterface(object):
    def serialise(self, records):
        def field_to_ext_type(field):
            internal_type = field.get_internal_type()

            # Obviously this isn't terribly comprehensive: string types can go
            # through as "auto", and field types beyond the standard set in
            # Django 1.1 aren't going to be handled gracefully. Still, it's a
            # start.
            MAPPING = {
                "AutoField": "int",
                "BooleanField": "boolean",
                "DateField": "date",
                "DateTimeField": "date",
                "FloatField": "float",
                "IntegerField": "int",
                "NullBooleanField": "boolean",
                "PositiveIntegerField": "int",
                "PositiveSmallIntegerField": "int",
                "SmallIntegerField": "int",
            }

            if internal_type in MAPPING:
                return MAPPING[internal_type]

            return "auto"

        rows = []
        for record in records:
            rows.append(self.serialise_record(record))

        def serialise_fields(model):
            fields = []

            for field in model._meta.fields:
                fields.append({
                    "name": field.name,
                    "type": field_to_ext_type(field),
                })

                try:
                    field.rel.to
                    fields.append({
                        "name": field.name + "__unicode",
                        "type": "string",
                    })
                except AttributeError:
                    pass

            return fields

        try:
            if callable(self.model.serialised_fields):
                fields = self.model.serialised_fields()
            else:
                fields = serialise_fields(self.model)
        except AttributeError:
            fields = serialise_fields(self.model)

        metadata = {
            "root": "rows",
            "idProperty": self.model._meta.pk.name,
            "successProperty": "success",
            "fields": fields
        }

        obj = {
            "metaData": metadata,
            "rows": rows,
        }

        return dumps(obj, indent=4, ensure_ascii=False)

    def serialise_record(self, record):
        def serialise_record(record):
            d = {}

            for field in record._meta.fields:
                # It's helpful to return both the primary key and string
                # representation of foreign keys.
                value = getattr(record, field.name)
                try:
                    # Test to see if we have a foreign key relationship.
                    field.rel.to

                    # The value might actually be None if it's nullable.
                    try:
                        d[field.name] = value.pk
                        d[field.name + "__unicode"] = unicode(value)
                    except AttributeError:
                        d[field.name] = None
                        d[field.name + "__unicode"] = u""
                except AttributeError:
                    # No foreign key relationship.
                    d[field.name] = unicode(value)

            return d

        serialiser = serialise_record
        try:
            if callable(self.model.serialise):
                serialiser = lambda record: record.serialise()
        except AttributeError:
            pass

        return serialiser(record)

    def set_field(self, instance, field, value):
        """Set a field on an instance of the ModelAdmin's model while
        respecting foreign keys. Surely there's an easier way to do this in
        Django, but I'll be damned if I can figure out how."""

        # Check if it's a foreign key: if so, we have to
        # instantiate the right object first.
        model_field = self.model._meta.get_field_by_name(field)[0]

        try:
            foreign_class = model_field.rel.to
            actual = foreign_class.objects.get(pk=value)
        except AttributeError:
            actual = value

        setattr(instance, field, actual)

    def get_urls(self):
        urls = super(ExtJsonInterface, self).get_urls()
        local_urls = patterns("",
            url(r"^ext/json/{0,1}$", self.admin_site.admin_view(self.root_dispatcher)),
            url(r"^ext/json/(?P<id>[0-9]+)$", self.admin_site.admin_view(self.id_dispatcher)),
        )
        return local_urls + urls

    def handle_create(self, request):
        o = self.model()
        
        # Pull in the JSON data that's been sent, if it is in fact JSON.
        try:
            row = loads(request.raw_post_data)["rows"]

            try:
                for field in row:
                    self.set_field(o, field, row[field])
            except Exception, e:
                print e

                response = {
                    "success": False,
                    "message": "Unable to parse incoming record.",
                }

                return HttpResponseBadRequest(content_type="text/plain; charset=UTF-8", content=dumps(response))
        except ValueError:
            for field in request.POST:
                self.set_field(o, field, request.POST[field])
        except KeyError:
            response = {
                "success": False,
                "message": "Unable to parse incoming record.",
            }

            return HttpResponseBadRequest(content_type="text/plain; charset=UTF-8", content=dumps(response))

        o.save(force_insert=True)

        response = {
            "success": True,
            "message": "Created new record.",
            "data": self.serialise_record(o),
        }

        return HttpResponse(content_type="text/plain; charset=UTF-8", content=dumps(response))

    def handle_delete(self, request, id):
        try:
            o = self.queryset(request).get(pk=id)
            o.delete()

            # If we've gotten here, all is well.
            transaction.commit()

            response = {
                "success": True,
                "message": "Record deleted.",
            }

            return HttpResponse(content_type="text/plain; charset=UTF-8", content=dumps(response))
        except self.model.DoesNotExist:
            transaction.rollback()

            response = {
                "success": False,
                "message": "The record could not be found.",
            }
            
            return HttpResponseNotFound(content_type="text/plain; charset=UTF-8", content=dumps(response))

    def handle_read(self, request):
        qs = self.queryset(request)

        # Add filters.
        filters = {}
        for field, term in request.GET.iteritems():
            if field not in ("sort", "dir", "_dc"):
                filters[smart_str(field)] = term

        if len(filters) > 0:
            try:
                qs = qs.filter(**filters)
            except FieldError:
                # Bad parameter to QuerySet.filter.
                return HttpResponseBadRequest(content_type="text/plain; charset=UTF-8", content=dumps("Bad search term"))

        # Apply sorting parameters, if given.
        if "sort" in request.GET and "dir" in request.GET:
            field = request.GET["sort"]
            if request.GET["dir"].lower() == "desc":
                field = "-" + field
            qs = qs.order_by(field)

        return HttpResponse(content_type="text/plain; charset=UTF-8", content=self.serialise(qs))

    @transaction.commit_manually
    def handle_update(self, request, id):
        try:
            # Grab the name of the primary key field.
            pk = self.model._meta.pk.name

            # Pull in the JSON data that's been sent.
            row = loads(request.raw_post_data)["rows"]
            qs = self.queryset(request)

            # OK, retrieve the object and update the field(s).
            o = qs.get(pk=row[pk])
            for name, value in row.iteritems():
                if name != pk:
                    self.set_field(o, name, value)
            o.save()

            # If we've gotten here, all is well.
            transaction.commit()

            response = {
                "success": True,
            }

            return HttpResponse(content_type="text/plain; charset=UTF-8", content=dumps(response))
        except self.model.DoesNotExist:
            transaction.rollback()

            response = {
                "success": False,
                "message": "The record could not be found.",
            }
            
            return HttpResponseNotFound(content_type="text/plain; charset=UTF-8", content=dumps(response))
        except KeyError:
            transaction.rollback()

            response = {
                "success": False,
                "message": "An internal error occurred.",
            }
            
            return HttpResponseServerError(content_type="text/plain; charset=UTF-8", content=dumps(response))
    
    def id_dispatcher(self, request, id):
        if request.method == "PUT":
            return self.handle_update(request, id)
        elif request.method == "DELETE":
            return self.handle_delete(request, id)
        else:
            return HttpResponseNotAllowed(["PUT", "DELETE"])

    def root_dispatcher(self, request):
        if request.method == "GET":
            return self.handle_read(request)
        elif request.method == "POST":
            return self.handle_create(request)
        else:
            # Unknown method.
            return HttpResponseNotAllowed(["GET", "POST"])
