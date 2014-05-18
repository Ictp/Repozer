<%inherit file="SearchBoxBase.tpl"/>

<%block name="searchExtras">
    <tr>
    <td style="text-align: right;">${ _("Search for")}</td>
    <td>

            <select class="UIFieldSpan" name="collections">
                <option value="" ${"selected" if collections=="" else ""}>${ _("Events")}</option>
                <option value="Contribution" ${"selected" if collections=="Contribution" else ""}>${ _("Contributions")}</option>
                <option value="Material" ${"selected" if collections=="Material" else ""}>${ _("Materials")}</option>
                <option value="All" ${"selected" if collections=="All" else ""}>${ _("All")}</option>
            </select>
    </td>
    </tr>
</%block>