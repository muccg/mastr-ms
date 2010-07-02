Ext.ns("MA.Dashboard");


MA.Dashboard.Component = Ext.extend(Ext.Panel, {
    constructor: function (config) {
        var defaultConfig = {
            defaults: {
                margins: "5px",
                split: true
            },
            layout: {
                type: "border"
            },
            items: [
                new MA.ProjectList({
                    title: "Projects",
                    region: "center",
                    listeners: {
                        "dblclick": MA.LoadProject
                    }
                }),
                new MA.RunList({
                    title: "Runs",
                    region: "east",
                    listeners: {
                        "dblclick": MA.LoadRun
                    }
                })
            ]
        };

        config = Ext.apply(defaultConfig, config);

        MA.Dashboard.Component.superclass.constructor.call(this, config);

        this.addEvents("project", "run");
    }
});


MA.DashboardCmp = new MA.Dashboard.Component({
    id: "dashboard",
    title: "Dashboard"
});


MA.Dashboard.prepare = function () {
    projectsListStore.load();

    runListStore.load();
    runListStore.sort([
        {
            field: "state",
            direction: "DESC"
        },
        {
            field: "id",
            direction: "DESC"
        }
    ]);
};
