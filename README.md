# WikiMap
A data visualization tool for Wikipedia.

The goal of this project is to create a visualization of Wikipedia starting with a page seed. The chosen page becomes the center of the map and nodes are created outwards in terms of degrees of separation.

Separation is determined by Wikipedia's backlinks. A backlink is a page that links to the current page. For example, if Page 1 has a link to Page 2, then Page 2 is chosen as the seed for the map, Page 1 would be one degree separated due to the immediate backlink.
