from django.conf.urls.defaults import patterns, url
from django.db import transaction
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseNotFound, HttpResponseServerError
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

        def serialise_record(record):
            d = {}

            for field in record._meta.fields:
                d[field.name] = unicode(getattr(record, field.name))

            return d

        serialiser = serialise_record
        try:
            if callable(self.model.serialise):
                serialiser = lambda record: record.serialise()
        except AttributeError:
            pass

        rows = []
        for record in records:
            rows.append(serialiser(record))

        fields = []
        for field in self.model._meta.fields:
            fields.append({
                "name": field.name,
                "type": field_to_ext_type(field),
            })

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

    def get_urls(self):
        urls = super(ExtJsonInterface, self).get_urls()
        local_urls = patterns("",
            url(r"^ext/json/{0,1}$", self.admin_site.admin_view(self.root_dispatcher)),
            url(r"^ext/json/(?P<id>[0-9]+)$", self.admin_site.admin_view(self.id_dispatcher)),
        )
        return local_urls + urls

    def handle_create(self, request):
        o = self.queryset(request).create()
        
        for field in request.POST:
            setattr(o, field, request.POST[field])

        o.save()

        response = {
            "success": True,
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
                "data": [],
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
                    setattr(o, name, value)
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
