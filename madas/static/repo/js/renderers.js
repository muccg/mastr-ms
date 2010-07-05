function renderSampleClass(value, p, record){
    var style = (value.active)?'':'text-decoration:strikethrough;';
    return String.format(
        '<div style="{0}"><b>{1}</b></div>', style,
            value.text);
}

function renderStatus(v, p, record) {
	var numeric = v;
    var value = "";
    if (numeric == "1") {
        value = "New";
    } else if (numeric == "2") {
        value = "Designed";
    }

	return value;
}

function renderSampleLogType(val) {
    switch (val) {
        case 0:
            return 'Received';
            break;
        case 1:
            return 'Stored';
            break;
        case 2:
            return 'Prepared';
            break;
        case 3:
            return 'Acquired';
            break;
        case 4:
            return 'Data Processed';
            break;
    }
    
    return '';
}

function renderRunProgress(val, meta, record) {
    var progress = record.get("complete_sample_count") / record.get("sample_count");

    if (isNaN(progress)) {
        progress = 0.0;
    }

    var progressBar = new Ext.ProgressBar({
        text: Math.floor(progress * 100.0).toString() + "%",
        value: progress
    });

    var id = Ext.id();
    
    (function () {
        if (Ext.get(id) != null) {
            progressBar.applyToMarkup(id);
        }
    }).defer(50);

    return "<div id='" + id + "'></div>";
}

function renderRunState(val) {
    var states = [
        "New",
        "In Progress",
        "Complete"
    ];

    return states[val];
}

function renderOrganism(val) {
    return renderValueOnly(organismComboStore, val);   
}

function renderLocation(val) {
    return renderValueOnly(locationComboStore, val);   
}


function renderTreatmentType(val) {
    return renderValueOnly(treatmentTypeComboStore, val);   
}

function renderUser(val) {
    return renderValueOnly(userComboStore, val);   
}

function renderClass(val) {
    return renderValueOnly(Ext.StoreMgr.get('classCombo'), val);   
}

function renderGenotype(val) {
    return renderValueOnly(genotypeComboStore, val);   
}

function renderLightSource(val) {
    return renderValueOnly(lightSourceComboStore, val);   
}

function renderInvolvement(val) {
    return renderValueOnly(involvementComboStore, val);   
}

var renderDate = Ext.util.Format.dateRenderer("d/m/Y");

var renderDateTime = Ext.util.Format.dateRenderer("d/m/Y H:i:s");

function renderValueOnly(store, val) {
   
    var results = store.queryBy(function(rec) {
        return rec.data.key == val;
    });
    
    if (results.getCount() < 1) {
        return '(not found)';
    }
    
    return results.itemAt(0).data.value;
}

function renderSOPLabel(val) {
   
    var results = sopLookupStore.queryBy(function(rec) {
        return rec.data.id == val;
    });
    
    if (results.getCount() < 1) {
        return '(not found)';
    }
    
    return results.itemAt(0).data.label;
}

function renderSOPDescription(val) {
   
    var results = sopLookupStore.queryBy(function(rec) {
        return rec.data.id == val;
    });
    
    if (results.getCount() < 1) {
        return '(not found)';
    }
    
    return results.itemAt(0).data.comment;
}

function renderNavItem(val, p, r) {
    if (!r.data.enabled) {
        return String.format('<div class="x-row-disabled">{0}</div>', val);
    }
    
    return val;
}
