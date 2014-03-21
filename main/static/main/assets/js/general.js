function rendermainpage(){
	$(".contain-page").load("/mainpage");
}
function rendertopmenu(){
	$(".header-wrap").load("/top_menu");
}
function homeclick(){
	$("#home").click(function(){
		$(".contain-page").load("/mainpage");
	});
}
function rendergrids(num_of_items, images, item_names, prices, ids){
		if(jQuery.type(num_of_items)!="number" || jQuery.type(images)!="array" || jQuery.type(item_names)!="array"|| jQuery.type(prices)!="array"){
			return false;
		}
		for ( var i = 0; i < num_of_items; i++ ) {
			var item = '<li> <a href="'+item_names[i] + "_" + ids[i] + '" id="item-img'+i+'"></a> <a href="'+item_names[i] + "_" + ids[i] +'" class="title">'+item_names[i]+'</a><strong>&dollar;'+prices[i]+'</strong></li>'
			$("#items").append(item);
			$("a#item-img"+i).html("<img src='"+images[i]+"'/>");
		}
		return true;
}
function capitaliseFirstLetter(string)
{
	if(string ==""){
		return "";
	}
    return string.charAt(0).toUpperCase() + string.slice(1);
}
function renderpage(desp, image, item_name, price){
	if(jQuery.type(desp)!="string" || jQuery.type(image)!="string" || jQuery.type(item_name)!="string"|| jQuery.type(price)!="number"){
		return false;
	}
	$("#price").html("&dollar;"+price);
	var current_category = capitaliseFirstLetter(window.location.pathname.split('/')[1]);
	$("#breadcrumb").html('<a href="/'+current_category+'">'+current_category+'</a> > '+item_name );
	$("h1#item_name").html(item_name );
	$("p#desp").html("Description: "+desp);
	$("div#images").html("<img src='"+image+"'/>");
	return true;
}
