function reserveSeat(myuid, seats, numSeats){
    var val = seats.value;
    if(val==="")
        return;

    var request = new XMLHttpRequest();
    request.onreadystatechange=function(){
        if(request.status=200 && request.readyState==4){
            //change button to text and make bold and green 
            var button=seats.parentNode;
            var theseat = $(button.parentNode).find("#numSeats");
            $(button).html('Seat Reserved');
            $(button).css('color', '#00FF00');
            $(button).css('fontWeight', 'bold');
            alert(numSeats);
            theseat.html(numSeats);

        }
    };

    request.open("POST","/updateRides",true);
    request.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    request.send('seats='+numSeats--);
    request.send(myuid);

}