<div class="container">
    % if searchingPublicWarning:
        <div class="searchPublicWarning" style="float: right;" >
        ${ _("Warning: since you are not logged in, only results from public events will appear.")}
        </div>
    % endif

    <h1 class="Search">Search ${ "Event" if confId else ("category" if categId !="0" else "") }</h1>

    <div class="topBar">
        <div class="content">

            <div class="SearchDiv">

                <div style="float: right; margin-top:10px;">
                    <span style="color:#777">Search powered by</span>
                    <%block name="banner">
                    </%block>
                </div>

                <form method="GET" action="${ searchAction }" style="width: 400px;">
                % if categId:
                    <input type="hidden" id="categId" name="categId" value="${ categId }"/>
                % endif
                % if confId:
                    <input type="hidden" name="confId" value="${ confId }"/>
                % endif
                
                
                <div>
                  <input style="width: 300px; height:20px; font-size:17px; vertical-align: middle;" type="text" name="p" value=${ quoteattr(p) } />
                  <input type="submit" value="${ _('Search')}" style="vertical-align: middle;"/>
                </div>

                <div style="padding-top: 4px;"><span id="advancedOptionsText" class='fakeLink'>${_("Show advanced options") }</span></div>
                <div id="advancedOptions" style="display: none;">
                    <table style="text-align: right;" id="advancedOptionsTable">
                      <tr>
                        <td>${ _("Search in") }:</td>
                        <td>
                          <select class="UIFieldSpan" name="f">
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
                        <td style="text-align: right;">${ _("Category")}:</td>
                        <td>
                            <select name="category">                  
                                <option value="" ${"selected" if category=="" else ""}>${ _("All")}</option>
                                % for cat in catnames:
                                    <option value="${cat}" ${"selected" if category==cat else ""}>${cat}</option>
                                % endfor
                                
                                

                            </select>
                        </td>
                    </tr>
                    <!-- /Ictp Specific -->

                    <tr>
                        <td style="text-align: right;">${ _("Use wildcards") }:</td>
                        <td>
                            <input type="checkbox" name="wildcards" value="wildcards" ${"checked" if wildcards=="wildcards" else ""} /> (will take longer...)
                        </td>
                    </tr>


                    <tr>
                        <td style="text-align: right;">${ _("Keywords")}:</td>
                        <td>
                            <input style="height:20px; width:180px; vertical-align: middle;" type="text" name="keywords" value="${keywords}" />
                        </td>
                    </tr> 
                      
                      <%block name="searchCollection">
                      </%block>
                      <tr>
                        <td>${ _("Start Date") }:</td>
                        <td>
                            <span id="startDatePlaceBox">
                                <input name="startDate" id="startDatePlace" type="text" style="width:180px" value="${startDate}"/>
                            </span>
                        </td>
                      </tr>
                      <tr>
                        <td>${ _("End Date") }:</td>
                        <td>
                            <span id="endDatePlaceBox">
                                <input name="endDate" id="endDatePlace" type="text"  style="width:180px" value="${endDate}"/>
                            </span>
                        </td>
                      </tr>
                      <%block name="searchSorting">
                      </%block>
                    </table>
                </div>
                </form>

            </div>
        </div>
        <%block name ="results">
        </%block>

    </div>
</div>

<script type="text/javascript">
    $("#advancedOptionsText").click(function(){
        if($("#advancedOptions").is(":hidden")){
            $("#advancedOptions").show();
            $("#advancedOptionsText").text($T("Hide advanced options"));
        }
        else{
            $("#advancedOptions").hide();
            $("#advancedOptionsText").text($T("Show advanced options"));
        }
    });

    $("#startDatePlace").datepicker({ dateFormat: "dd/mm/yy", firstDay: 1, defaultDate:"${startDate}",changeMonth: true,
      changeYear: true});
    $("#endDatePlace").datepicker({ dateFormat: "dd/mm/yy",  firstDay: 1, defaultDate:"${endDate}",changeMonth: true,
      changeYear: true});
    
    
</script>

<%block name ="scripts">
</%block>


