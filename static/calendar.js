function calendar(curr_month)
{
	//holds the current month which will be used to go to the previous or next month
	document.curr_month = curr_month;
	
	//create date object
	var date = new Date();
	
	//set the month from the input param
	date.setMonth(curr_month);
	//get important attributes from object
	var day = date.getDate();
	var month = date.getMonth();
	var year = date.getYear();
	
	//not sure why we need to do this
	if(year<=200)
	{
			year += 1900;
	}
	
	//create months array and days in months
	months = new Array('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December');
	days_in_month = new Array(31,28,31,30,31,30,31,31,30,31,30,31);
	
	//leap year?
	if(year%4 == 0 && year!=1900)
	{
			days_in_month[1]=29;
	}
	
	//total days in present month
	total = days_in_month[month];
	
	
	//variable for the title of the calendar
	var date_today = months[month]+' '+year;
	
	//create table and first row
	var text = '';
	text += ('<table class="cal_calendar"><tbody id="cal_body"><tr>');
	//create previous month button
	text += ('<td class="button_td"><button type="submit" class="button" onmouseover="highlight(this);" onclick="prevMonth(this);" id="'+month+'">Previous Month</button></td>');
	//create title for calendar
	text += ('<th colspan="5" id="date">'+date_today+'</th>');
	//create next month button
	text += ('<td class="button_td"><button type="submit" class="button" onmouseover="highlight(this);" onclick="nextMonth(this);" id="'+month+'">Next Month</button></td></tr>');
	//create week label headers
	text += ('<tr class="cal_weeks"><th>Sunday</th><th>Monday</th><th>Tuesday</th><th>Wednesday</th><th>Thursday</th><th>Friday</th><th>Saturday</th></tr><tr>');
	
	//will help determine what day (mon, tues...) the 1st of this month will fall on
	var beginning = date;
	
	//sets the day to be the first of the current month
	beginning.setDate(1);
	
	//gets the day of the week the first falls on
	the_first = beginning.getDay();
	the_first_copy = the_first;
	
	//set today's day
	var d_copy = new Date();
	today = d_copy.getDate();
	today_month = d_copy.getMonth();
	next_weeks = 0;
	
	for(weeks = 0; weeks < 6; weeks++){  //rows for the calendar
	
		text += ('<tr>');
		num = 0; //num is the number of times we added a date from the previous month
		
		for(days = 1, numdays = 0; days < 8; days++) //cols for calendar
		{	
			
			if(the_first > 0)  //fills in the previous months days
			{
				if(month == 0){
					
					text += ('<td class="cal_prev_month_days" onmouseover="highlight(this);" onmouseout="unhighlight(this);" onclick="handleClick(this);" id="'+(31-(the_first-1))+','+(11)+'">'+(31-(the_first-1))+'</td>');
				}
				else{
					text += ('<td class="cal_prev_month_days" onmouseover="highlight(this);" onmouseout="unhighlight(this);" onclick="handleClick(this);" id="'+(days_in_month[month-1]-(the_first-1))+','+(month-1)+'">'+(days_in_month[month-1]-(the_first-1))+'</td>');
				}
				the_first--;
				num++;
			}
			else if( (7*weeks)+days-(the_first_copy) <= total) //are there more days?
			{	
				numdays++;
				
				
				if((7*weeks)+days-(the_first_copy) == today && today_month == month) //is this day today?
				{ 
					if(weeks == 0){ //if it is still the first week, don't subtract when the day the 1st started
						text += ('<td class="today" onmouseover="highlight(this);" onmouseout="unhighlight(this);" onclick="handleClick(this);" id="'+((7*weeks)+days-num)+','+(month)+'">'+((7*weeks)+days-num)+'</td>');
					}
					else{
						//this day is today, change the class name for CSS
						text += ('<td class="today" onmouseover="highlight(this);" onmouseout="unhighlight(this);" onclick="handleClick(this);" id="'+((7*weeks)+days-num-the_first_copy)+','+(month)+'">'+((7*weeks)+days-num-the_first_copy)+'</td>');
					}
				}
				
				else
				{  //this day is not today, normal CSS name
				
					if(weeks == 0){ //if it is still the first week, don't subtract when the day the 1st started
						text += ('<td class="cal_days" onmouseover="highlight(this);" onmouseout="unhighlight(this);" onclick="handleClick(this);" id="'+((7*weeks)+days-num)+','+(month)+'">'+((7*weeks)+days-num)+'</td>');
					}
					else{
						text += ('<td class="cal_days" onmouseover="highlight(this);" onmouseout="unhighlight(this);" onclick="handleClick(this);" id="'+((7*weeks)+days-num-the_first_copy)+','+(month)+'">'+((7*weeks)+days-num-the_first_copy)+'</td>');
					}
				}
				if((7*weeks)+days-(the_first_copy) == total){
					weeks = 6;
				}
			}
			
			else{ //no more days in this month, start writing for the next month, don't need to worry about num since that only effects the first week
				if(month == 11){
					text += ('<td class="cal_next_month_days" onmouseover="highlight(this);" onmouseout="unhighlight(this);" onclick="handleClick(this);" id="'+((7*next_weeks)+days-numdays)+','+(0)+'" >'+((7*next_weeks)+days-numdays)+'</td>');
				}
				else{
					text += ('<td class="cal_next_month_days" onmouseover="highlight(this);" onmouseout="unhighlight(this);" onclick="handleClick(this);" id="'+((7*next_weeks)+days-numdays)+','+(month+1)+'" >'+((7*next_weeks)+days-numdays)+'</td>');
				}
				
				if(days == 7){
					weeks = 6;
				}
			}
		}
		
		text += ('</tr>');
	
	}
	text += ('</tbody></table>');
	
	document.getElementById('my-calendar').innerHTML = text;
	
	return true;
}

function handleClick(elem){
	
	location.replace("list_rides");
}

function highlight(tag) 
{
	tag.style.cursor = "pointer";
}

function unhighlight(tag)
{
	//nothing here for now
}

function prevMonth(elem)
{
	document.curr_month--;
	calendar(document.curr_month);
}

function nextMonth(elem)
{
	document.curr_month++;
	calendar(document.curr_month);
}





