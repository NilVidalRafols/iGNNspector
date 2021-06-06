var graph = {
    name: "",
    is_saved: false
};

var stages = [
    function () { // graph selection
        // $('#explorer').slideToggle("slow");
        // $('#saved-explorer').slideToggle("slow");
        $('analyse-btn').prop('disabled', true);
        $('#stage-0').slideDown('slow');
        $('#stage-1').slideUp('slow');
        $('#stage-2').slideUp('slow');
        $('#stage-3').slideUp('slow');

    },
    function () { // analyse graph in the background and notify the user
        $('#stage-0').slideUp('slow');
        $('#stage-1').slideDown('slow');
        $('#stage-2').slideUp('slow');
        $('#stage-3').slideUp('slow');
    },
    function () { // show results of the analysis and give the user the possibility to download results
        $('#stage-0').slideUp('slow');
        $('#stage-1').slideUp('slow');
        $('#stage-2').slideDown('slow');
        $('#stage-3').slideUp('slow');
    },
    function () { // Proposals
        $('#stage-0').slideUp('slow');
        $('#stage-1').slideUp('slow');
        $('#stage-2').slideUp('slow');
        $('#stage-3').slideDown('slow');
    },
]

var stage = 0;

$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip({
        placement : 'right'
    });
    // this button triggers stage 0
    $('#browse-btn').click(function () {
        set_stage(0);
        eel.request_paths($(this).attr('value'));
        $('#explorer').slideToggle("slow");
    });
    // this button triggers stage 1
    $('#analyse-btn').click(function () {
        set_stage(1);
        var name = $('#selected-graph').text();
        if (name)
            eel.analyze_graph(graph.name, graph.is_saved);
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
    $('#analyse-btn').prop('disabled', false);
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

eel.expose(message)
function message(name) {
    if (name == '')
        $('.message').hide();
    else
        $(name).show();
}

eel.expose(set_stage)
function set_stage(index) {
    stages[index]();
}