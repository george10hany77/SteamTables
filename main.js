function update(e){
    const supers = e.textContent;
    e.parentElement.parentElement.parentElement.querySelector("span").textContent= ""+supers
}




function man(e){
    let version = e.parentElement.parentElement.parentElement.className.split(" ")[1]
    if(version == "two"){
        version ="one"
    }else{
        version = "two"
    }

    // let type = e.className.split[" "][1];
    update(e);
}