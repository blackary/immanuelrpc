function lastIndexOf(str, toFind) { 
    var index = str.indexOf(toFind);
    if(index == -1) return -1;
    while(index != -1) {
        prevIndex = index;
        index = str.indexOf(toFind, index+1);
    }
    return prevIndex;
}

function doinit() {
    $('loading').hide();
    new Effect.Appear('doc', {duration: 1.5});
    var pageID = getPageID();
    top.curPage = pageID;
    top.curSubmenu = null;
    top.hasSubmenu = {"home":false, "about_us":true, "worship":true, "calendar":false, "contact":false, 'mission':false, 'identity':false, 'conviction':false, 'leaders':false, 'services':false, 'approach':false, 'sermons':false, 'location':false}; 
    top.menuParent = {"home":null, "about_us":null, "worship":null, "calendar":null, "contact":null, 'mission':'about_us', 'identity':'about_us', 'conviction':'about_us', 'leaders':'about_us', 'services':'worship', 'approach':'worship', 'sermons':'worship', 'location':'worship'};    
    doclick($(pageID));
}

function loadIframe(iframeID, iframeSRC) {
    $(iframeID).src = iframeSRC;
}

/*
function loadIframes() {
    //'iframe_google_cal':'http://www.google.com/calendar/embed?src=bcsl9pmoc7sr2l1ohifiujin40%40group.calendar.google.com',
    //'iframe_sermon_audio':'sermons.html',    
    var iframes = {

        'iframe_shorter_cat':'shorter_cat.htm',   
        'iframe_larger_cat':'larger_cat.htm',
        'iframe_confession':'confession.htm',
        'iframe_covenant':'covenant_of_membership.htm'
    };

    var timeout = 100;
    for(var iframeID in iframes) {
        setTimeout("loadIframe('" + iframeID + "','" + iframes[iframeID] + "')", timeout);
        timeout += 100;
    }
}*/

function dohover(div) {
    var id = div.id;
    div.addClassName("menu_hover");
}

function doleave(div) {
    var id = div.id;
    if(id != top.curPage) {
        div.removeClassName("menu_hover");
    }
}

function doclick(div) {
    
    var id = div.id;    

    if(top.hasSubmenu[id]) {
        
        var subMenu = 'sub_menu_'+id;
        //alert(top.curSubmenu + " : " + subMenu);
        if(top.curSubmenu == subMenu) {
            return;
        }
        if(top.curSubmenu) {
            new Effect.BlindUp($(top.curSubmenu), {duration: .3});
        }
        new Effect.BlindDown($('sub_menu_'+id), {duration: .3});

        top.curSubmenu = subMenu;

    } else {
        var subMenu = 'sub_menu_'+top.menuParent[id];

        var newContentDiv = id + "_content";
        //window.location.hash = id;
        $("content").innerHTML = $(newContentDiv).innerHTML;      

        $(top.curPage).removeClassName("menu_hover");
        $(id).addClassName("menu_hover");
        
        $('hl_'+top.curPage).hide();
        new Effect.Appear('hl_'+id, {duration: 1});

        top.curPage = id;
        scroll(0, 0);
    
        if(top.curSubmenu != subMenu) {
            if(top.curSubmenu) {
                new Effect.BlindUp($(top.curSubmenu), {duration: .3});
                top.curSubmenu = null;
            } else {
                new Effect.BlindDown($(subMenu), {duration: .3});
                top.curSubmenu = subMenu;
            }
        }        
        top.curThumbnail = 'loc_img_8';
        
        pageTracker._trackPageview(top.curPage);
    }
}

function open_expander(id) {
    var expanderDiv = $(id);
    var isOpenID = 'expander_'+id;
    if (top[isOpenID] == true) {
        top[isOpenID] = false;
        new Effect.BlindUp(expanderDiv, {duration: .3});
    } else {
        top[isOpenID] = true;        
        new Effect.BlindDown(expanderDiv, {duration: .3});
    }
    pageTracker._trackPageview(id);    
}

function show_text(id) {
    $('hl_'+top.curPage).hide();
    $('content').innerHTML = $(id + '_content').innerHTML;
    pageTracker._trackPageview(id);    
}

function hide_text() {
    $('hl_'+top.curPage).show();
    $('content').innerHTML = $(top.curPage + '_content').innerHTML;
}

function getPageID() {
    var pageID = window.location.hash ? window.location.hash.replace('#','') : 'home'; 
    if (window.location.search.indexOf('sa_action') != -1) {
        pageID = 'sermons';   
    }
    return pageID;
}

function location_swap_image(thumbID) {
    thumbID = $(thumbID).id;
    var divID = thumbID.replace('thumb', 'img');
    $(top.curThumbnail).hide();
    new Effect.Appear(divID, {duration: 0.75});    
    top.curThumbnail = divID;
}

