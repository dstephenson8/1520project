function reserveSeat(seats){
    var val = seats.value;
    if(val==="")
        return;

    var request = new XMLHttpRequest();
    request.onreadystatechange=function(){
        if(request.status=200 && request.readyState==4){
            //change button to text and make bold and green 
            var button=seats.parentNode;
            $(button).html('Seat Reserved');
            $(button).css('color', '#00FF00');
            $(button).css('fontWeight', 'bold');

        }
    };

    request.open("POST","/listing_of_rides",true);
    request.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    request.send('seats='+val);

}