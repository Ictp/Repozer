<form method="get" action="${searchAction}" id="searchBoxForm" style="margin: 0px;">
<input type="hidden" id="searchCategId" name="categId" value="0" data-current="${targetId}" data-current-name="${categName}"/>
<input type="hidden" name="sortOrder" value="d"/>
<div id="UISearchBox">
    <div id="searchControls">
        <div class="searchButton">

        </div>
        <div id="moreOptions" class="${ moreOptionsClass }" onclick="javascript:return expandMenu(this);"></div>
        <input style="background-color: transparent;" type="text" id="searchText" name="p" />
</div>

    <div id="extraOptions">
        <div id="advancedOptionsLabel">${ _("Advanced options")}</div>
        <table id="extraOptionsTable">
        <tr>
                <td style="text-align: right;">${ _("Search in")}</td>
                <td>
                    <select name="f">
                        <option value="title_description" ${"selected" if f=="title_description" else ""}>${ _("Title and Description")}</option>
                        <option value="" ${"selected" if f=="" else ""}>${ _("Title only")}</option>
                        <option value="roles" ${"selected" if f=="roles" else ""}>${ _("Roles")}</option>

                        <!--<option value="abstract">${ _("Talk description/Abstract")}</option>-->
                        <!--<option value="author">${ _("Author/Speaker")}</option>-->
                        <!--<option value="affiliation">${ _("Affiliation")}</option>-->
                        <!--<option value="fulltext">${ _("Fulltext")}</option>-->
                        <!--<option value="keyword">${ _("Keyword")}</option>-->
                    </select>
                </td>
            </tr>
            
            
            <!-- Ictp Specific: Hard coded Category fields. Can be removed or replaced with full text input box -->
            <tr>
                <td style="text-align: right;">${ _("Category")}</td>
                <td>
                 
                    <select name="category">                  
                        <option value="" ${"selected" if category=="" else ""}>${ _("All")}</option>
                        <option value="Activities in Trieste" ${"selected" if category=="Activities in Trieste" else ""}>${ _("Activities in Trieste")}</option>
                        <option value="Activities outside Trieste" ${"selected" if category=="Activities outside Trieste" else ""}>${ _("Activities outside Trieste")}</option>
                        <option value="Seminars" ${"selected" if category=="Seminars" else ""}>${ _("Seminars")}</option>
                        <option value="Hosted activities" ${"selected" if category=="Hosted activities" else ""}>${ _("Hosted activities")}</option>
                    </select>                                             

                </td>
            </tr>
            <!-- /Ictp Specific -->



            <tr>
                <td style="text-align: right;">${ _("Start Date")}</td>
                <td>
                    <span id="startDatePlaceBox">
                      <input name="startDate" id="startDate" type="text" />
                    </span>
                </td>
            </tr>
            <tr>
                <td style="text-align: right;">${ _("End Date")}</td>
                <td>
                    <span id="endDatePlaceBox">
                      <input name="endDate" id="endDate" type="text" />
                    </span>
                </td>
            </tr>
        </table>
    </div>
</div>
</form>

<script type="text/javascript">

function expandMenu(domElem)
{
    var elem = new XElement(domElem);

    if(!exists(elem.dom.extraShown))
    {
        var controls = searchControls;
        $('#extraOptions').width($('#searchControls').width()).slideDown('fast');
        $('#extraOptions').position({
            of: $('#searchControls'),
            my: 'right top',
            at: 'right bottom'
        });
        elem.dom.extraShown=true;
        resetForm();
    }
    else
    {
        $('#extraOptions').slideUp('fast');
        elem.dom.extraShown=null;
        resetForm();

    }
    return false;
}



function resetForm()
{
    // reset all the fields, except the phrase
    var text = $E('searchText').dom.value;
    $E('searchBoxForm').dom.reset();
    $E('searchText').dom.value = text;

}

function verifyForm()
{
    var startDate = $('#startDate').val();
    var endDate = $('#endDate').val();
    return (!startDate || Util.parseDateTime(startDate, IndicoDateTimeFormats.DefaultHourless)) &&
        (!endDate || Util.parseDateTime(endDate, IndicoDateTimeFormats.DefaultHourless));
}


var searchControls = $E('searchControls');

var intelligentSearchBox = new IntelligentSearchBox({name: 'p', id: 'searchText',
                                 style: {backgroundColor: 'transparent', outline: 'none'}
                 }, $E('UISearchBox'), $E('searchSubmit'));


$(function() {
    $('#startDate').datepicker({ dateFormat: "dd/mm/yy", firstDay:1 });
    $('#endDate').datepicker({ dateFormat: "dd/mm/yy", firstDay:1 });

    $E('searchText').replaceWith(
        intelligentSearchBox.draw()
    );

    var where = $('#searchCategId').data('current');
    var target_title = $('#searchCategId').data('current-name');

    $('.searchButton').click(function() {
        if (verifyForm()) {
            $('#searchBoxForm').submit();
        };
    })

    $('#searchText').keypress(function(e) {
        if(e.which == 13 && !intelligentSearchBox.isAnyItemSelected()){
            if (verifyForm()) {
                $('#searchBoxForm').submit();
            }
        }
    });

    if (where != '0') {
        $('.searchButton', '#searchBoxForm').before($('<div class="searchTag"/>'));
        $('.searchTag').search_tag({
            everywhere: true,
            categ_title: target_title,
            categ_id: where,
            input: $('#searchCategId')
        });
    }
});

</script>
