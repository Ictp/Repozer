<%inherit file="SearchResultBase.tpl"/>
<%block name="banner">
    <a href="http://docs.repoze.org/catalog/"><img src="${searchIcon}" alt="repoze.catalog" title="${ _("IndicoSearch is powered by repoze.catalog")}" style="vertical-align: middle; border: 0px;" /></a>
</%block>

<%block name="searchCollection">
    <tr>
        <td>${ _("Search for") }:</td>
        <td>
            <select class="UIFieldSpan" name="collections">
                <option value="" ${"selected" if collections=="" else ""}>${ _("Events")}</option>
                <option value="Contribution" ${"selected" if collections=="Contribution" else ""}>${ _("Contributions")}</option>
                <!--<option value="Material" ${"selected" if collections=="Material" else ""}>${ _("Materials")}</option>-->
                <option value="All" ${"selected" if collections=="All" else ""}>${ _("All")}</option>
            </select>
        </td>
    </tr>
</%block>



<%block name="searchSorting">
    <tr>
        <td>${ _("Sort field") }:</td>
        <td>
            <select class="UIFieldSpan" name="sortField" style="display: inline;">
                <option value="" ${"selected" if sortField=="" else ""}>${ _("Date")}</option>
                <option value="titleSorter" ${"selected" if sortField=="titleSorter" else ""}>${ _("Title")}</option>
          </select>
        </td>
    </tr>
    <tr>
        <td>${ _("Sort order") }:</td>
        <td>
            <select class="UIFieldSpan" name="sortOrder" style="display: inline;">
                <option value="a" ${"selected" if sortOrder=="a" else ""}>${ _("Ascending")}</option>
                <option value="d" ${"selected" if sortOrder=="d" else ""}>${ _("Descending")}</option>
            </select>
        </td>
    </tr>
</%block>

<%block name ="results">

    <%include file="SearchNavigationForm.tpl" args="target = 'Events', direction='Next'"/>
    <%include file="SearchNavigationForm.tpl" args="target = 'Contributions', direction='Next'"/>
    <%include file="SearchNavigationForm.tpl" args="target = 'Events', direction='Prev'"/>
    <%include file="SearchNavigationForm.tpl" args="target = 'Contributions', direction='Prev'"/>

    % if p != '':
        <h3 style="float:right;margin:0px;">Hits: ${ numHits }</h3>
    % endif

    <div id="container" style="clear:both;">
        % if len(eventResults) > 0:
            <div id="events">
                <%include file="SearchNavigationBar.tpl" args="target = 'Events', shortResult = evtShortResult"/>

                <ul class="searchResultList">
                    % for result in eventResults:
                    <%include file="SearchResultEntry.tpl" args="accessWrapper=accessWrapper, result=result"/>
                    % endfor
                </ul>
                <%include file="SearchNavigationBar.tpl" args="target = 'Events', shortResult = evtShortResult"/>
            </div>
        % endif

        % if len(contribResults) > 0:
            <div id="contribs">
                <%include file="SearchNavigationBar.tpl" args="target = 'Contributions', shortResult = contShortResult"/>
                <ul class="searchResultList">
                    % for result in contribResults:
                    <%include file="SearchResultEntry.tpl" args="accessWrapper=accessWrapper, result=result"/>
                    % endfor
                </ul>
                <%include file="SearchNavigationBar.tpl" args="target = 'Contributions', shortResult = contShortResult"/>
            </div>
        % endif
    </div>

    % if len(contribResults) == 0 and len(eventResults) == 0 and p != '':
        <div style="margin-top: 20px; color: red;">No results found</div>
    % endif
</%block>

<%block name="scripts">
    <script type="text/javascript">
        $(function(){

            % if len(eventResults) > 0 or len(contribResults) > 0:
                var tabList = [];

                % if len(eventResults) > 0:
                    tabList.push([$T('Events'), $E('events')]);
                % endif
                % if len(contribResults) > 0:
                    tabList.push([$T('Contributions'), $E('contribs')]);
                % endif
            
                // Don't display tabs
                //var tabCtrl = new JTabWidget(tabList);
                //$E('container').set(tabCtrl.draw());
                //$('#container>div').css({"display":"table", "width":"100%"});

            % endif

            });
    </script>
</%block>