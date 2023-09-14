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


function filterItemsByStock(items) {
    var filteredItems = [];

    for (var i = 0; i < items.length; i++) {
        var item = items[i];

        if (item.stock < item.min_stock) {
            filteredItems.push(item);
        }
    }

    return filteredItems;
}



function print_inform(){
    var doc=new jsPDF();

    // console.log(items);
    
    // items = filterItemsByStock(items);

    // console.log(items);

    // // Definir el formato de la plantilla
    // var margin = 10;
    // var lineHeight = 10;
    
    // // Agregar el logotipo
    // var logoUrl = "C:\Documentos\Santi Pedemonte PC\Cursos\CS50W\CS50W - GitHub\capstone\item_track\assets\item_track\Logo versión negro.png"
    // var logoWidth = 50;
    // var logoHeight = 30; 
    // var logoX = margin;
    // var logoY = margin;
    // doc.addImage(logoUrl, 'PNG', logoX, logoY, logoWidth, logoHeight);
    
    // // Título
    // doc.setFontSize(18);
    // doc.text("Pedido de Mercadería", margin, margin + lineHeight + logoHeight);
    
    // for (var i = 0; i < items.length; i++) {
    //     // Información del artículo
    //     doc.setFontSize(12);
    //     doc.text("Nombre del Artículo: " + item.name, margin, margin + 2 * lineHeight + logoHeight);
    //     doc.text("Cantidad en Stock: " + item.stock, margin, margin + 3 * lineHeight + logoHeight);
    //     doc.text("Cantidad Mínima en Stock: " + item.stock_min, margin, margin + 4 * lineHeight + logoHeight);    
    // }

    // doc.save("test.pdf")
    print()
}
