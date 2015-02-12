function calendar(curr_month)
{
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
	document.write('<table class="cal_calendar"><tbody id="cal_body"><tr>');
	//create previous month button
	document.write('<td class="button_td"><button type="submit" class="button" onmouseover="highlight(this);" onclick="prevMonth(this);" id="'+month+'">Previous Month</button></td>');
	//create title for calendar
	document.write('<th colspan="5" id="date">'+date_today+'</th>');
	//create next month button
	document.write('<td class="button_td"><button type="submit" class="button" onmouseover="highlight(this);" onclick="nextMonth(this);" id="'+month+'">Next Month</button></td></tr>');
	//create week label headers
	document.write('<tr class="cal_weeks"><th>Sunday</th><th>Monday</th><th>Tuesday</th><th>Wednesday</th><th>Thursday</th><th>Friday</th><th>Saturday</th></tr><tr>');
	
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
	
		document.write('<tr>');
		num = 0; //num is the number of times we added a date from the previous month
		
		for(days = 1, numdays = 0; days < 8; days++) //cols for calendar
		{	
			
			if(the_first > 0)  //fills in the previous months days
			{
				if(month == 0){
					
					document.write('<td class="cal_prev_month_days" onmouseover="highlight(this);" onmouseout="unhighlight(this);" onclick="handleClick(this);" id="'+(31-(the_first-1))+','+(11)+'">'+(31-(the_first-1))+'</td>');
				}
				else{
					document.write('<td class="cal_prev_month_days" onmouseover="highlight(this);" onmouseout="unhighlight(this);" onclick="handleClick(this);" id="'+(days_in_month[month-1]-(the_first-1))+','+(month-1)+'">'+(days_in_month[month-1]-(the_first-1))+'</td>');
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
						document.write('<td class="today" onmouseover="highlight(this);" onmouseout="unhighlight(this);" onclick="handleClick(this);" id="'+((7*weeks)+days-num)+','+(month)+'">'+((7*weeks)+days-num)+'</td>');
					}
					else{
						//this day is today, change the class name for CSS
						document.write('<td class="today" onmouseover="highlight(this);" onmouseout="unhighlight(this);" onclick="handleClick(this);" id="'+((7*weeks)+days-num-the_first_copy)+','+(month)+'">'+((7*weeks)+days-num-the_first_copy)+'</td>');
					}
				}
				
				else
				{  //this day is not today, normal CSS name
				
					if(weeks == 0){ //if it is still the first week, don't subtract when the day the 1st started
						document.write('<td class="cal_days" onmouseover="highlight(this);" onmouseout="unhighlight(this);" onclick="handleClick(this);" id="'+((7*weeks)+days-num)+','+(month)+'">'+((7*weeks)+days-num)+'</td>');
					}
					else{
						document.write('<td class="cal_days" onmouseover="highlight(this);" onmouseout="unhighlight(this);" onclick="handleClick(this);" id="'+((7*weeks)+days-num-the_first_copy)+','+(month)+'">'+((7*weeks)+days-num-the_first_copy)+'</td>');
					}
				}
			}
			
			else{ //no more days in this month, start writing for the next month, don't need to worry about num since that only effects the first week
				document.write('<td class="cal_next_month_days" onmouseover="highlight(this);" onmouseout="unhighlight(this);" onclick="handleClick(this);" id="'+((7*next_weeks)+days-numdays)+','+(month+1)+'" >'+((7*next_weeks)+days-numdays)+'</td>');
				if(days == 7){
					next_weeks++;
				}
			}
		}
		
		document.write('</tr>');
	
	}
	
	document.write('</tbody></table>');
	
	return true;
}

function handleClick(elem){
	var id = elem.id; //get the day and then the month
	var partsOfStr = id.split(',');
	window.alert("The month is: " + months[partsOfStr[1]] + "\nThe day is: " + partsOfStr[0]);
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
	var id = elem.id;
	id_int = parseInt(id);
	id_int--;
	if(id_int <0){
		id_int = 11;
	}
	//alert(id_int);
	document.write(calendar(id_int));
}

function nextMonth(elem)
{
	var id = elem.id;
	id_int = parseInt(id);
	id_int++;
	if(id_int > 11){
		id_int = 0;
	}
	//alert(id_int);
	document.write(calendar(id_int));
}





