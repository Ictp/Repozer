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

                <form method="GET" action="${ searchAction }" style="width: 500px;">
                % if categId:
                    <input type="hidden" id="categId" name="categId" value="${ categId }"/>
                % endif
                % if confId:
                    <input type="hidden" name="confId" value="${ confId }"/>
                % endif
                
                <div>
                    <h6>Text search will search for exact words. </h6>
                    <h6>To search for substrings, use "*". Eg: "math*"</h6>

                </div>
                <div>
                  <input style="width: 300px; font-size:17px; vertical-align: middle;" type="text" name="p" value=${ quoteattr(p) } />
                  <input type="submit" value="${ _('Search')}" style="vertical-align: middle;"/>
                </div>

                <div style="padding-top: 4px;"><span id="advancedOptionsText" class='fakeLink'>${_("Show advanced options") }</span></div>
                <div id="advancedOptions" style="display: none;">
                    
                    <table style="text-align: right;" id="advancedOptionsTable">
                      <tr>
                        <td>${ _("Search in") }:</td>
                        <td>
                          <select class="UIFieldSpan" name="f" style="width: 100%;">
                            <option value="" ${"selected" if f=="" else ""}>${ _("Title and Description")}</option>
                            <option value="title_only" ${"selected" if f=="title_only" else ""}>${ _("Title only")}</option>
                            <option value="roles" ${"selected" if f=="roles" else ""}>${ _("Roles")}</option>
                            <option value="persons" ${"selected" if f=="persons" else ""}>${ _("Speakers/Chairmans")}</option>
                            <option value="all" ${"selected" if f=="all" else ""}>${ _("All")}</option>
                          </select>
                        </td>
                      </tr>



                      <%block name="searchCollection"></%block>


                                            
                    <tr>
                        <td style="text-align: right;">${ _("Category")}:</td>
                        <td>
                            <select name="category" style="width: 100%;">                  
                                <option value="" ${"selected" if category=="" else ""}>${ _("All")}</option>
                                % for catkey in categories.keys():
                                    <option value="${catkey}" ${"selected" if category==catkey else ""}>${categories[catkey]}</option>
                                % endfor
                            </select>
                        </td>
                    </tr>


<!--

                    <tr>
                        <td style="text-align: right;">${ _("Keyword")}:</td>
                        <td>
                            <select name="keywords" id="keywords">                  
                                <option value="" ${"selected" if keyword=="" else ""}>${ _("All")}</option>
                                % for keyw in avakeywords:
                                    <option class="itemTool" value="${keyw}" title="${keyw}" ${"selected" if keywords==keyw else ""}>
                                        % if len(keyw) < 30:
                                            ${keyw}
                                        % endif
                                        % if len(keyw) >= 30:
                                            ${keyw[:27]}...
                                        % endif                                    
                                    </option>
                                % endfor
                            </select>
                            
                        </td>
                    </tr> 
-->                      

                      
                      
                      <tr>
                        <td>${ _("Between dates") }:</td>
                        <td>
                            <span id="startDatePlaceBox">
                                <input name="startDate" id="startDatePlace" type="text" style="width:90px;" value="${startDate}"/>
                            </span>
                            and 
                            <span id="endDatePlaceBox">
                                <input name="endDate" id="endDatePlace" type="text"  style="width:90px;" value="${endDate}"/>
                            </span>
                            

                        </td>
                      </tr>
                      
                      
                      <%block name="searchSorting"></%block>
                      
                      
                      <tr>
                        <td>${ _("Limit results to") }:</td>
                        <td>
                            <select name="limit" id="limit" style="width:100%;">                  
                                <option value="" ${"selected" if limit=="" else ""}>250</option>
                                <option value="1000" ${"selected" if limit=="1000" else ""}>1000</option>
                                <option value="unlimited" ${"selected" if limit=="unlimited" else ""}>unlimited</option>                                
                            </select>
                        </td>
                      </tr>
                      
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
    % if len(eventResults) == 0:
    // Start showing advanced options
    $( "#advancedOptionsText" ).trigger( "click" );
    % endif

    $("#startDatePlace").datepicker({ dateFormat: "dd/mm/yy", firstDay: 1, defaultDate:"${startDate}",changeMonth: true,
      changeYear: true});
    $("#endDatePlace").datepicker({ dateFormat: "dd/mm/yy",  firstDay: 1, defaultDate:"${endDate}",changeMonth: true,
      changeYear: true});
    
</script>






