/*
    <div id = "menuitem1"> item 1 </div>
    <div id = "menuitem2"> item 2 </div>
    <div id = "menuitem3"> item 3 </div>
            
    menu example: 
        new JSButton("menuitem_1", {
                group: "mymenu",
                up: "menuUp",
                down: "menuDown",
                hover: "menuHover",
                onclick: function() { alert("item 1 selected ") }
            });


        new JSButton("menuitem_1", {
                group: "mymenu",
                up: "menuUp",
                down: "menuDown",
                hover: "menuHover",
                onclick: function() { alert("item 2 selected ") },
                selected: "selected"
            });

        new JSButton("menuitem_1", {
                group: "mymenu",
                up: "menuUp",
                down: "menuDown",
                hover: "menuHover",
                onclick: function() { alert("item 3 selected ") }
            });

*/



var JSButton = Class.create({
    initialize: function(id, params) {
        
        
        this.id = id;
        this.div = $(id);         
        this.div.jsButton = this; // setup back reference
                    
        if(params['group']){
            buttonManager.add(id, params['group']);            
            this.group = params['group'];

        }
        
        if(params['up']){
            this.up = params['up'];
        }

        if(params['down']){
            this.down = params['down'];
        }

        if(params['hover']){
            this.hover = params['hover'];
        }

        if(params['selected'] && params['selected'] == 'selected') {
            this.isSelected = true;
            this.doClick();
        } else {
            this.isSelected = false;
            this.doDeselect();
        }

        if(params['onclick']) {
            this.clickAction = params['onclick'];
            this.div.observe('click', this.clickAction.bind(this));
        }
        
        this.div.observe('mouseover', this.doHover.bind(this));
        this.div.observe('mouseout', this.doLeave.bind(this));
        this.div.observe('click', this.doClick.bind(this));        

    },
    doHover: function() {
        this.clearCSS();
        if(this.hover) {
            this.div.addClassName(this.hover);
        } else {
            this.div.addClassName(this.down);
        }
    }, 
    doLeave: function() {
        if(!this.isSelected) {
            this.clearCSS();
            this.div.addClassName(this.up);
        }
        this.isSelected = false;
    }, 
    doClick: function() {
        this.clearCSS();
        this.div.addClassName(this.down);
        this.isSelected = true;
        buttonManager.deselect(this.group, this.id);
    },
    doDeselect: function() {
        this.clearCSS();
        this.div.addClassName(this.up);
    },
    clearCSS: function(){
        this.div.setAttribute("class", "");
    }
});


var ButtonManager = Class.create({
    initialize: function() {
        this.groups = {};
    }, 
    add: function(id, group) {
        // ensure group exists
        if(!this.groups[group])
            this.groups[group] = [];
        
        // add id to group
        this.groups[group].push(id);
    },
    deselect: function(group, idToSelect) {
        group = this.groups[group];
        // if the button is part of a group
        if (group) {
            // then loop through the other buttons in the group
            $A(group).each(function(id){
                if(id != idToSelect) {
                    // and deselect them
                    $(id).jsButton.doDeselect();
                }
            }.bind(this));
        }
    }
});

var buttonManager = new ButtonManager();



