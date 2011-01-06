Ext.ns("MA.Dashboard");


MA.Dashboard.Component = Ext.extend(Ext.Panel, {
    constructor: function (config) {
        var defaultConfig = {
            border:false,
            defaults: {
                margins: "5px",
                split: true,
                border: false
            },
            layout: {
                type: "border"
            },
            items: [
                new MA.ProjectList({
                    title: "Projects",
                    region: "center",
                    width: "50%",
                    listeners: {
                        "dblclick": MA.LoadProject
                    }
                }),
                new MA.RunList({
                    title: "Runs",
                    region: "east",
                    width: "50%",
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
    id: "dashboard"
});


MA.Dashboard.prepare = function () {
    MA.Authorize('auth:auth');

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
