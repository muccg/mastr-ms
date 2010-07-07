MA.InlineSearch = Ext.extend(Ext.Panel, {
    constructor: function (config) {
        var self = this;

        var defaultConfig = {
            bodyStyle: "background: transparent; border: none; text-align: left",
            layout: "hbox",
            items: [
                new Ext.form.TextField({
                    itemId: "inline-search",
                    flex: 1,
                    enableKeyEvents: true,
                    listeners: {
                        "change": function () { self.update(); },
                        "keyup": function () { self.update(); }
                    }
                }),
                new Ext.Button({
                    itemId: "clear-inline-search",
                    flex: 0,
                    icon: "static/repo/images/clear.png",
                    tooltip: "Clear search",
                    handler: function () {
                        self.getComponent("inline-search").setValue("");
                        self.update();
                    }
                })
            ]
        };

        config = Ext.apply(defaultConfig, config);

        if (config.filterFunction) {
            this.filterFunction = config.filterFunction;
        }
        else {
            throw new Ext.Error("Inline search requires a filtering function.");
        }

        if (config.store) {
            /* Augment the store so we can track search terms across inline
             * search instances. */
            this.store = config.store;
            this.store.inlineSearch = {
                term: ""
            };

            /* Listen for datachanged events so we can track filter
             * application. */
            this.store.addListener("datachanged", function () {
                var searchBox = self.getComponent("inline-search");

                // Override if there's no filter applied.
                if (this.isFiltered()) {
                    searchBox.setValue(this.inlineSearch.term);
                }
                else {
                    searchBox.setValue("");
                }
            });
        }
        else {
            throw new Ext.Error("Inline search requires a store to be provided.");
        }

        MA.InlineSearch.superclass.constructor.call(this, config);
        this.addEvents("clear", "search");
    },
    update: function () {
        var self = this;
        var searchBox = this.getComponent("inline-search");
        var value = searchBox.getValue();

        this.store.inlineSearch.term = value;

        if (value) {
            this.store.filterBy(function (record, id) {
                return self.filterFunction(record, value);
            });
            this.fireEvent("search", value);
        }
        else {
            this.store.clearFilter();
            this.fireEvent("clear");
        }
    }
});
