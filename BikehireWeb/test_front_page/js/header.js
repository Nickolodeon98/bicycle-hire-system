
$(function() {
    $('input[name="daterange"]').daterangepicker({
        opens: 'left',
        minDate:new Date()
    }, function(start, end, label) {
        console.log("A new date selection was made: " + start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD'));

    });
});
