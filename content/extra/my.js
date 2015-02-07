// Add link picture
var article_block=$("article");

// Add link icon
$("a:not([href^='http://www.hitsumabushi.org']):not([href^='#']):not([class^='addthis_'])",  article_block).after("<i class=\"fa fa-link\"></i>");

