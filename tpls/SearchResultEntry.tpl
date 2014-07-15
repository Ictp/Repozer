<%page args="accessWrapper=None, result=None"/>
<% import MaKaC %>

<li class="${"searchResultEvent" if type(result) == ConferenceEntry else "searchResultContribution"}">
    % if result.getTitle():
        <a class="searchResultTitle" href="${ result.getURL().replace('%','%%') }">        
        ${result.getTitle()}
        </a>
    % endif    
    % if result.getStartDate(accessWrapper):
         <small style="display: block;">${ result.getStartDate(accessWrapper).strftime("%Y-%m-%d %H:%M:%S (%Z)") }</small>
    % endif
    % if not isinstance(result.getTarget(),MaKaC.conference.Conference):
         <span style="display: block; font-style:italic; font-size:x-small;">${ result.getConference().getTitle()}</span>
    %endif
    
<%
if result.getDescription() != None:
    fullDesc = result.getDescription()
    entryDesc = truncateTitle(result.getDescriptionText(), maxSize=300)
else:
    fullDesc = entryDesc = ''

try:
    entryDesc = entryDesc.encode('iso8859-1','replace')
except:
    entryDesc = entryDesc.encode('utf8','replace')

%>

    <div class="searchResultDescription">
        ${ entryDesc }
    </div>


</li>
