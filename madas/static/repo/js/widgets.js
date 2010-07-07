MA.InlineSearch = Ext.extend(Ext.Panel, {
    constructor: function (config) {
        var self = this;

        var defaultConfig = {
            bodyStyle: "background: transparent; border: none",
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
                    handler: function () {
                        self.getComponent("inline-search").setValue("");
                        self.update();
                    }
                })
            ]
        };

        config = Ext.apply(defaultConfig, config);

        MA.InlineSearch.superclass.constructor.call(this, config);
        this.addEvents("clear", "search");
    },
    update: function () {
        var searchBox = this.getComponent("inline-search");
        var value = searchBox.getValue();

        if (value) {
            this.fireEvent("search", value);
        }
        else {
            this.fireEvent("clear");
        }
    }
});
