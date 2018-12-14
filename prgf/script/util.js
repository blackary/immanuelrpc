function doInit() {
  top.selectedId = 'conviction';
  menuClick('conviction');
}

function menuClick(id) {
  id = $(id).id;
  var div = $(id+'_content'); 
  $('copy').hide();
  $('copy').innerHTML = div.innerHTML;
  new Effect.Appear('copy', {duration: 0.75});
  setMenuImage(top.selectedId, top.selectedId+'.png');  
  setMenuImage(id, id+'_hover.png');
  top.selectedId = id;  
}

function menuMouseOver(id) {
  id = $(id).id;
  setMenuImage(id, id+'_hover.png');
}

function menuMouseOut(id) {
  id = $(id).id;
  if(top.selectedId != id) {
    setMenuImage(id, id+'.png');
  }
}

function setMenuImage(id, imgName) {
  var div = $(id);
  var img = div.down();
  img.src = 'images/'+imgName;
}