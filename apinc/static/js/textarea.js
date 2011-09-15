/*
*   Copyright © 2011 APINC Devel Team
*
*   This program is free software; you can redistribute it and/or modify
*   it under the terms of the GNU General Public License as published by
*   the Free Software Foundation; either version 2 of the License, or
*   (at your option) any later version.
*
*   This program is distributed in the hope that it will be useful,
*   but WITHOUT ANY WARRANTY; without even the implied warranty of
*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*   GNU General Public License for more details.
*
*   You should have received a copy of the GNU General Public License
*   along with this program; if not, write to the Free Software
*   Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
*
*/

// http://files.wymeditor.org/wymeditor/trunk/src/examples/
$(document).ready(function() {
    var wym_options = {};
    var wym_defaults = { updateSelector:":submit", updateEvent:"click", logoHtml:'', };
    var wym_custom = {
        postInit: function(wym) {
            //render the containers box as a panel
            //and remove the span containing the '>'
            jQuery(wym._box).find(wym._options.containersSelector)
                .removeClass('wym_dropdown')
                .addClass('wym_panel')
                .find('h2 > span')
                .remove();
            //adjust the editor's height
            jQuery(wym._box).find(wym._options.iframeSelector)
            .css('height', '350px');
        },
        classesHtml: [], // On garde seulement le panel 'Containers'
        /*
         * classesItems: [
         * {'name': 'date', 'title': 'PARA: Date', 'expr': 'p'},
         * {'name': 'hidden-note', 'title': 'PARA: Hidden note', 'expr': 'p[@class!="important"]'}
         * ],
         *
         */
    };

    $.extend(wym_options, wym_defaults, wym_custom);
    $("textarea").wymeditor(wym_options);
    }
);
