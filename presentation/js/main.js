var graph = {
    name: "",
    is_saved: false
};



$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip({
        placement : 'right'
    });

    $('#browse-btn').click(function () {
        eel.request_paths($(this).attr('value'));
        $('#explorer').slideToggle("slow")
    });

    $('#select-btn').click(function () {
        name = $('#selected-graph').text()
        if (name)
            eel.set_graph(graph.name, graph.is_saved)
    });

    eel.request_saved_reports();
});

eel.expose(set_paths);
function set_paths(content) {
    $('#explorer table tbody').html(content);
    $('#explorer table tbody tr').each(function () {
        $(this).click(function () {
            eel.request_paths($(this).attr('value'));
        });
    });
}

eel.expose(set_graph)
function set_graph(name, is_saved) {
    graph.name = name
    graph.is_saved = is_saved
    $('#selected-graph').text(name);
    $('#select-btn').prop('disabled', false);
}

eel.expose(set_saved_reports)
function set_saved_reports(content) {
    $('#saved-explorer table tbody').html(content);
    $('#saved-explorer table tbody tr').each(function () {
        $(this).click(function () {
            set_graph($(this).attr('value'), true);
        });
    });

}

