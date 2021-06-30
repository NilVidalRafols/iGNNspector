var graph = {
    name: "",
    is_saved: false,
    time: 0.0,
    split_size: 0,
    num_splits: 0,
    report: {}
};

var proposal = {
    index: ''
}

var stages = [
    // STAGE 0: graph selection
    function () {
        // $('#explorer').slideToggle("slow");
        // $('#saved-explorer').slideToggle("slow");
        $('analyse-btn').prop('disabled', true);
        $('save-analysis-btn').prop('disabled', true);
        $('#stage-0').slideDown('slow');
        $('#stage-1').slideUp('slow');
        $('#stage-2').slideUp('slow');
        $('#stage-3').slideUp('slow');

    },
    // STAGE 1: analyse graph in the background and notify the user
    function () {
        $('#stage-0').slideUp('slow');
        $('#stage-1').slideDown('slow');
        $('#stage-2').slideUp('slow');
        $('#stage-3').slideUp('slow');
    },
    // STAGE 2: show results of the analysis and give the user the possibility 
    // to download results
    function () {
        if (!graph.is_saved)
            enable_button('#save-analysis-btn', true);
        $('#stage-0').slideUp('slow');
        $('#stage-1').slideUp('slow');
        $('#stage-2').slideDown('slow');
        $('#stage-3').slideUp('slow');
    },
    function () { // STAGE 3: Proposals
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
    // The app starts in STAGE 0
    set_stage(0);
    // this button triggers STAGE 0
    $('#browse-btn').click(function () {
        set_stage(0);
        eel.request_paths($(this).attr('value'));
        $('#explorer').slideToggle("slow");
    });
    // this button triggers STAGE 1
    $('#analyse-btn').click(function () {
        set_stage(1);
        var name = $('#selected-graph').text();
        if (name) {
            if ($('#time-camps').is(':visible')) {
                value = $('#time-camps').val();
                eel.analyse_graph(graph.name, 
                                graph.is_saved, 
                                {time: $('#analysis-time').val()});
            } else {
                value = $('#split-camps').val();
                eel.analyse_graph(graph.name, 
                                graph.is_saved, 
                                {   split_size: $('#split-size').val(),
                                    num_splits: $('#num-splits').val()});
            }
        }
    });
    // this button saves the analysis report
    $('#save-analysis-btn').click(function () {
        eel.save_analysis();
    });
    // assign camps to show when clicking these buttons
    $('#time-btn').click(function () {
        $('#time-camps').show();
        $('#split-camps').hide();
    });
    $('#split-btn').click(function () {
        $('#time-camps').hide();
        $('#split-camps').show();
    });
    $('[data-toggle="popover"]').popover()

    // when changing these camps check if propose-btn can be enabled
    $('#input-features').click(function () {
        enable_proposal_button();
    });
    $('#output-features').click(function () {
        enable_proposal_button();
    });
    $('input[name=taskradio]').click(function () {
        enable_proposal_button();
    });

    // propose models when clicking propose-btn
    $('#propose-btn').click(function () {
        preferences = []
        if ($('#check1').is(':checked'))
            preferences.push('memory_efficiency');
        if ($('#check2').is(':checked'))
            preferences.push('time_efficiency');
        if ($('#check3').is(':checked'))
            preferences.push('accuracy');

        proposal_settings = {
            'input': $('#input-features').val(),
            'output': $('#output-features').val(),
            'task': $('input[name=taskradio]').val(),
            'preferences': preferences
        };
        eel.propose_models(proposal_settings);
    });
    // save proposal when clicking save-proposal-btn
    $('#save-proposal-btn').click(function () {
        eel.save_proposal(proposal[index]);
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
    graph.name = name;
    graph.is_saved = is_saved;
    $('#selected-graph').text(name);
    $('#analyse-btn').prop('disabled', false);
}

eel.expose(set_graph_report)
function set_graph_report(content) {
    $('#report-explorer table tbody').html(content);
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

eel.expose(set_proposal_table)
function set_proposal_table(content) {
    $('#proposal-table table tbody').html(content);
    $('#proposal-table table tbody tr').each(function () {
        $(this).click(function () {
            set_proposal($(this).attr('value'));
        });
    });

}

function set_proposal(index) {
    proposal['index'] = index;
    enable_button('#save-proposal-btn', proposal.index != '');
    enable_button('#build-btn', proposal.index != '');
}

function enable_proposal_button() {
    input = $('#input-features').val() > 0;
    output = $('#output-features').val() > 0;
    task = $('input[name=taskradio]').val() == "node_classification";
    stage_2 = $('#stage-2').is(':visible');
    enable_button('#propose-btn', input && output && task && stage_2);
}

eel.expose(message)
function message(id) {
    if (id == '')
        $('.message').hide();
    else
        $(id).show();
}

eel.expose(enable_button)
function enable_button(id, enable) {
    $(id).prop('disabled', !enable);
}

eel.expose(set_stage)
function set_stage(index) {
    stages[index]();
    message('');
    enable_proposal_button();
    enable_button('#save-analysis-btn', index == 2);
    enable_button('#save-proposal-btn', proposal.index != '');
    enable_button('#build-btn', proposal.index != '');
}