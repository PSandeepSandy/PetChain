function createDropDownList(name, list) {
    var htmlString = "<datalist id='"+name+"_dropdown'>";
    for(var i=0; i<list.length; i++) {
        htmlString = htmlString + '<option value="'+list[i]+'">'+list[i]+'</option>';
    }
    htmlString = htmlString + '</datalist>';
    return htmlString;
}

$(document).ready(function() {

    // $('.post_ad_form').toggle();

    $('.item_type_button').click(function(event) {
        item_type_text = $(this).text().trim();
        
        // Set the value of the hidden input field item_type 
        $('#item_type_field').val(item_type_text);
        
        // request data from server to get item attributes
        $.ajax({
            url: '/seller/post-ad/get-item-attr',
            data: {
                item_type: item_type_text
            },
        })
        .done(function(item_attr) {
            for (var i=0; i<item_attr.length; i++) {
                name = item_attr[i]['attr_name'];
                values = item_attr[i]['values'];
                var htmlCode = createDropDownList(name, values);
                $('#item_attrib_wrap').append('<p>'+name+': <input list="'+name+'_dropdown" name="'+ name + '_attr"></p>');
                $('#item_attrib_wrap').append(htmlCode);
            }
        });

        // request data from server to get invalid fields
        // hide those fields
        $.ajax({
            url: '/seller/post-ad/get-invalid-fields',
            data: {
                item_type: item_type_text
            },
        })
        .done(function(data) {
            // if (data) {
            //     fields = data['invalid_fields'];

            //     // Will hide all invalid fields
            //     for (var i=0; i<fields.length; i++) {
            //         $('#'+fields[i]+'_field').toggle();
            //     }
            // }
        })
        
    });
});