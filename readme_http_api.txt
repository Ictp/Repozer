http://indico.ictp.it/indico/export/conference/search.xml?today=2013/04/10
.xml  : export type, can be: .xml/.json/.html/.atom
today : if present, return all conferences which startDate <= today AND endDate >= today (running conferences)

OTHER PARAMETERS:
- start_date : return conferences where startDate >= start_date

- end_date   : return conferences where endDate <= end_date
eg: [..]/search.xml?start_date=2013/01/10
eg: [..]/search.xml?start_date=2013/04/10&end_date=2013/04/10
NB: start_date and end_date are ALTERNATIVE to today

- keywords : return confs with specific keyword. Can be a list. OR applied to keyword lists.
eg: [..]/search.xml?keywords=Phyiscs and Development,Condensed Matter and Statistical Physics

- category : return confs with specific category. Can be a list. 
eg: [..]/search.xml?category=2l132

- todaybeyond : return all conferences which startDate <= today AND endDate >= today (running conferences) AND future ones, where startData >= today
eg: same as today

- keywordsAnd : return confs with specific keywords joined by AND.
eg: [..]&keywordsAnd=Phyiscs and Development,Condensed Matter and Statistical Physics
As a result BOTH keywords must be presents

- limit : return first N results. Eg: [..]&limit=10 

- detail : specify output details level. Default: events

Options: events, contributions, subcontributions, sessions
eg: http://indico.ictp.it/indico/export/conference/search.xml?today=2013/04/10&detail=contributions 
