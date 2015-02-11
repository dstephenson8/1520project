function calendar()
{
        var date = new Date();
        var day = date.getDate();
        var month = date.getMonth();
        var year = date.getYear();
        if(year<=200)
        {
                year += 1900;
        }
        months = new Array('January', 'February', 'March', 'April', 'May', 'June', 'Jully', 'August', 'September', 'October', 'November', 'December');
        days_in_month = new Array(31,28,31,30,31,30,31,31,30,31,30,31);
        if(year%4 == 0 && year!=1900)
        {
                days_in_month[1]=29;
        }
		
        total = days_in_month[month];
        var date_today = months[month]+' '+year;
		
		
		
		
        beg_j = date;
        beg_j.setDate(1);
        if(beg_j.getDate()==2)
        {
                beg_j=setDate(0);
        }
        beg_j = beg_j.getDay();
        document.write('<table class="cal_calendar"><tbody id="cal_body"><tr><th colspan="7" id="date">'+date_today+'</th></tr>');
        document.write('<tr class="cal_weeks"><th>Sunday</th><th>Monday</th><th>Tuesday</th><th>Wednesday</th><th>Thursday</th><th>Friday</th><th>Saturday</th></tr><tr>');
        week = 0;
        for(i=1;i<=beg_j;i++)
        {
                document.write('<td class="cal_days">'+(days_in_month[month-1]-beg_j+i)+'</td>');
                week++;
        }
        for(i=1;i<=total;i++)
        {
                if(week==0)
                {
                        document.write('<tr>');
                }
                if(day==i)
                {
                        document.write('<td id="today" onmouseover="highlight(this);" onmouseout="unhighlight(this);" onclick="handleClick();">'+i+'</td>');
                }
                else
                {
                        document.write('<td onmouseover="highlight(this);" onmouseout="unhighlight(this);" onclick="handleClick();">'+i+'</td>');
                }
                week++;
                if(week==7)
                {
                        document.write('</tr>');
                        week=0;
                }
        }
        for(i=1;week!=0;i++)
        {
                document.write('<td class="cal_days" onmouseover="highlight(this);" onmouseout="unhighlight(this);" onclick="handleClick();">'+i+'</td>');
                week++;
                if(week==7)
                {
                        document.write('</tr>');
                        week=0;
                }
        }
        document.write('</tbody></table>');
		
        return true;
}
function handleClick(){
	/*document.location="http://google.com"  */
	
	
}
function highlight(tag) 
{
	tag.style.backgroundColor = '';
}
      
function unhighlight(tag) {
	tag.style.backgroundColor = '';
}