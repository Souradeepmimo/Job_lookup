
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

        Firstname           =   response_values[i][0]
        Lastname            =   response_values[i][1]
        Email               =   response_values[i][2]
        Phone               =   response_values[i][3]
        Skillset            =   response_values[i][4]
        
        row.push(Firstname)
        row.push(Lastname)
        row.push(Email)
        row.push(Phone)
        row.push(Skillset)
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
        //console.log(response)
        values=response.Answer
        console.log(values)
        renderTheTable(values)
    })
}
fetchjobdetails()
function sendApiRequest(){
    return new Promise(function(resolve, reject){
        const xhr=new XMLHttpRequest()  
        const link=`/Skilljoin`
        xhr.open('GET',link)
        
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

