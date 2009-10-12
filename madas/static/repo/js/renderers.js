function renderSampleClass(value, p, record){
    var style = (value.active)?'':'text-decoration:strikethrough;';
    return String.format(
        '<div style="{0}"><b>{1}</b></div>', style,
            value.text);
}

function renderProgress(v, p, record) {
	var text_post = '%';
	
	if(this.text){
        text_post = this.text;
    }
	var text_front;
	var text_back;
	
    if (!Ext.isDefined(v)) {
        v = '';
    }
    
	text_front = (v <55)?'':v+text_post;
	text_back = (v >=55)?'':v+text_post;		

	return String.format('<div class="x-progress-wrap" style="height:14px;"><div class="x-progress-inner"><div class="x-progress-bar" style="width:{0}%;"><div class="x-progress-text" style="width:100%;height:12px;">{1}</div></div><div class="x-progress-text x-progress-text-back" style="width:100%;">{2}</div></div></div>',v,text_front,text_back);		
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