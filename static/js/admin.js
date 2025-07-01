$(document).ready(function() {
    var listOfElements = $('select[id^="id_productFeature-"][id$="-features"]')
    $(listOfElements).on('change',function() {
        f_id = $(this).val();
        dd1 = $(this).attr('id');
        dd2 = dd1.replace("-features", "-filter_value");

        $.ajax({
            type: "GET",
            url: "/main_products/features_admin/?feature_id=" + f_id,
            success: function(res) {
                cols = document.getElementById(dd2);
                cols.options.length = 0;
                for (var k in res) {
                    cols.options.add(new Option(k, res[k]));
                }
            }
        });
    });
});


