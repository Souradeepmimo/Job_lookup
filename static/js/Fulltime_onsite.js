//const Searchbutton  =document.getElementById("Search")
//const Type          =document.querySelector("#Type")

var table1;
$(document).ready(function(){

    table1=$('#myTable').DataTable({
        
    })
})

function renderTheTable(response_values){
    new_values=[]
    for(i=0;i<response_values.length;i++){
        row=[]
        console.log(response_values[i])
        Email               =response_values[i]['Email']
        Job_requirement_id  =response_values[i]['Job Requirement Id']
        Date_               =response_values[i]['Date']
        Location_           =response_values[i]['Location']
        Type_               =response_values[i]['Type']
        job_description     =response_values[i]['Job Description']
        required_skills     =response_values[i]['Required Skills'].toString();
        status_              =response_values[i]['Status']

        row.push(Email)
        row.push(Job_requirement_id)
        row.push(Date_)
        row.push(Location_)
        row.push(Type_)
        row.push(job_description)
        row.push(required_skills)
        row.push(status_)
        console.log("row=",row)
        new_values.push(row)
    }

    table1.clear().draw();
    console.log(new_values)
    table1.rows.add(new_values).draw()
}


function fetchjobdetails(){
    sendApiRequest()
    .then(function(response){
        console.log(response)
        values=response.Answer

        values=JSON.parse(values)

        renderTheTable(values)
    })
}
fetchjobdetails()
function sendApiRequest(){
    return new Promise(function(resolve, reject){
        const xhr=new XMLHttpRequest()  
        const link=`/OnSiteFullTimeJob`
        console.log(link)
        //const params=`Type=${Type_}`;
        //console.log(params)
        xhr.open('GET',link)
        //xhr.setRequestHeader('Content-type','x-www-form-urlencoded')

        xhr.onload=function(){
            if(xhr.status==200){
                resolve(JSON.parse(xhr.responseText))
            }
            else{
                reject(xhr.statusText)
            }
        }
        xhr.onerror=function(){
            reject(xhr.statusText)
        }
        xhr.send()
    })

}

