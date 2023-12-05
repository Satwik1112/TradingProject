csv_file = document.getElementById("csv_file");

function show_message(notification){
    message = document.getElementById("message");
    message.innerText = notification;
}

function upload_to_server(file){
    // fetch a django server url here
    url = 'upload_file';
    show_message(notification="checking file...")
    fetch(
        url, {
            method: 'POST',
            headers: {
                'Content-Type': 'text/plain',
                'File-Size': file.size,
                'File-Name': file.name
                },
            body: file,
        }
    ).then(response=>{
        if (response.ok){
            return response.json();
        } else{
            throw new Error('cannot get proper response!')
        }
    })
    .then(data => {
        // giving condition for message to user
        if (data.message == "already uploaded"){
            show_message(notification="file is already uploaded!");
        }
        else if(data.message == "error while processing"){
            show_message(notification="something went wrong while processing file!");
        }
        else if(data.message == "uploaded and processed"){
            show_message(notification="file is already ready!");
            // check it's file extension
            filename = file.name.split(".");
            temp = filename.slice(0, -1);  // list of contents of file name
            save_json_file(temp.join(""), data.filedata);
        }
        else{
            show_message(notification="file is not uploaded!");
        }
    })
    .catch(error=>{console.log("error while uploading file", error);});
}

function save_json_file(filename, filedata){
    // build a download element and create a download button
    download_button = document.getElementById("download");
    message.innerHTML = `<span>Take JSON file `+filename+`.json</span>`
    const download = document.createElement('a');
    download.setAttribute('href',
    'data:application/json;charset=utf-8,'+
    encodeURIComponent(JSON.stringify(filedata)));
    download.setAttribute('download', filename+".json");
    download.setAttribute('id', "download-json");
    download.innerText = "Download"
    download_button.appendChild(download);
}


function handelTextFile(event){
    if (event.target.files.length == 1){
        file = event.target.files[0]; // get file object
        if(file.type === "text/plain"){
            // only for text file
            show_message(notification="file is uploading...")
            file_info = document.getElementById("file_info"); // for displaying file information
            file_info.innerText = file.name;
            upload_to_server(file);
        }
        else{
            // handle all other types files
            show_message(notification="file is not supported!")
        }
    }
}

csv_file.addEventListener("change", handelTextFile);
