function renderSampleClass(value, p, record){
    var style = (value.active)?'':'text-decoration:strikethrough;';
    return String.format(
        '<div style="{0}"><b>{1}</b></div>', style,
            value.text);
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
    // Always Ignore the val, here because ExtJS can't pass it in
    // the progress is calculated and not sent through in the JSON
    var progress = 0.0;
    if (Ext.isDefined(record)) {
        if (record.get("state") == 2) { // Completed
            progress = 1.0;
        } 
        else {
            progress = record.get("complete_sample_count") / record.get("sample_count");
        }
    }
    if (isNaN(progress)) {
        progress = 0.0;
    }

    return renderRunProgressBar(progress * 100.0);
}

function renderNoRunProgress() {
    return renderRunProgressBar(0);
}

function renderCompleteRunProgress() {
    return renderRunProgressBar(100);
}

function renderRunProgressBar(percent) {
    var percent = Math.floor(percent);
    var text = percent.toString() + "%";

    return "<div class='x-progress-wrap'>"
        + "<div class='x-progress-inner'>"
        + "<div style='position: relative; height: 16px; width: " + text + "' class='x-progress-bar'>"
        + "</div>"
        + "<div style='width: 100%; padding: 1px 0' class='x-progress-text'>"
        + "<div class='x-renderer-progress-text'>" + text + "</div>"
        + "</div>"
        + "</div>"
        + "</div>"
        + "</div>"
        + "</div>";
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
    return renderValueOnly(maStaffComboStore, val);   
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
