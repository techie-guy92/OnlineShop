status_of_cart()

function status_of_cart(){
    $.ajax({
        type:"GET",
        url:"/main_shopping_cart/status_of_cart/",
        success: function(res){
            $("#indicator__value").text(res);
        }
    });
};


function add_to_cart(product_id,qty){
    if (qty===0){
        qty=$("#product-quantity").val();
        // alert(qty);
    }
    $.ajax({
        type:"GET",
        url:"/main_shopping_cart/add_to_cart/",
        data:{
            product_id:product_id,
            qty:qty,
        },
        success: function(res){
            // alert("کالا اظافه شد");
            status_of_cart()
        }
    });
};


function del_from_cart(product_id){
    $.ajax({
        type:"GET",
        url:"/main_shopping_cart/del_from_cart/",
        data:{
            product_id:product_id,
        },
        success: function(res){
            $("#list_of_shopping_cart").html(res);
            status_of_cart()
        }
    });
};


function update_cart(){
    var list_of_product_id = []
    var list_of_qty = []
    $("input[id^='qty_']"). each(function(index){
        list_of_product_id.push($(this).attr('id').slice(4));
        list_of_qty.push($(this).val())
    });
    $.ajax({
        type:"GET",
        url:"/main_shopping_cart/update_cart/",
        data:{
            list_of_product_id : list_of_product_id,
            list_of_qty : list_of_qty,
        },
        success: function(res){
            // alert("list fetched");
            $("#list_of_shopping_cart").html(res);
            status_of_cart()
        }
    });
};


function ShowComments(product_Id,comment_Id,slug){
    $.ajax({
        type:"GET",
        url:"/hub/making_comment/" + slug,
        data:{
            product_Id:product_Id,
            comment_Id:comment_Id,
        },
        success: function(res){
            $("#btn_" + comment_Id).hide();
            $("#comment_form_" + comment_Id).html(res);
        }
    });
};


function giving_score(score,product_Id){
    var make_full_stars = document.querySelectorAll(".fa-star");

    make_full_stars.forEach(element => {
        element.classList.remove("checked");
    });

    for (let i=1; i <= score; i++){
        const element = document.getElementById("star_" + i);
        element.classList.add("checked");
    }

    $.ajax({
        type: "GET",
        url: "/hub/giving_score/",
        data: {
            product_Id: product_Id,
            score: score,
        },
        success: function(res){
            location.reload()
        }
    });

    make_full_stars.forEach(element => {
        element.classList.add("disable")
    }); 
};


function add_to_wish_list(product_Id){
    $.ajax({
        type:"GET",
        url:"/hub/add_to_wish_list/",
        data:{
            product_Id:product_Id,
        },
        success: function(res){
            location.reload()
            status_of_wish_list()
        }
    })
};


status_of_comparison_list();


function status_of_comparison_list(){
    $.ajax({
        type:"GET",
        url:"/main_products/status_of_comparison_list/",
        success: function(res){
           if (Number(res) == 0){
                $("#comparison_icon").hide();
           } else{
               $("#comparison_icon").show();
               $("#comparison_count").text(res);
           }
        }
    })
};


function add_to_comparison_list(product_Id,groupId){
    $.ajax({
        type:"GET",
        url:"/main_products/add_to_comparison_list/",
        data:{
            product_Id:product_Id,
            groupId:groupId,
        },
        success: function(res){
            status_of_comparison_list()
        }
    })
};


function del_from_comparison_list(product_Id){
    $.ajax({
        type:"GET",
        url:"/main_products/del_from_comparison_list/",
        data:{
            product_Id:product_Id,
        },
        success: function(res){
            $("#comparison_list").html(res)
            status_of_comparison_list()
        }
    })
};