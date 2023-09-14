function all_items(){
    document.getElementById("all-items").classList.add("active");
    document.getElementById("re-stock-item").classList.remove("active");

    var items = document.getElementsByClassName("with-stock");
    for (var i = 0; i < items.length; i++) {
        items[i].style.display = "block";
    }
}

function re_stock(){
    document.getElementById("all-items").classList.remove("active");
    document.getElementById("re-stock-item").classList.add("active");

    var items = document.getElementsByClassName("with-stock");
    for (var i = 0; i < items.length; i++) {
        items[i].style.display = "none";
    }
}

function print_inform(){
    var doc=new jsPDF();
    doc.text(20,20, "PDF")
    doc.save("test.pdf")
}
