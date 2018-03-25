This is a listing of what the UI may look like, and of what it will/does look like.

<!-- TOC depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Organization views](#organization-views)
	- [What does the Org need?](#what-does-the-org-need)
		- [Org Needs List view](#org-needs-list-view)
	- [What are people donating?](#what-are-people-donating)
		- [Org Donators List view](#org-donators-list-view)
		- [Org Donators Map view](#org-donators-map-view)
- [Driver views](#driver-views)
	- [Whilst driving 1](#whilst-driving-1)
- [Donator views](#donator-views)
	- [Donator Inventory View](#donator-inventory-view)
- [ER Diagrams](#er-diagrams)
	- [User-House-Items relationship](#user-house-items-relationship)
- [Miscellaneous views](#miscellaneous-views)
	- [Data JSON to HTML element](#data-json-to-html-element)
		- [What we need it to look like](#what-we-need-it-to-look-like)
		- [Recusive implementation](#recusive-implementation)

<!-- /TOC -->

# Screenshots

## Donator UI

![A view of a single home.](homeview.PNG)

![A view allowing one to edit a home.](edithome.PNG)

![A view listing the items you own in a home.](itemsview.PNG)

![A view showing someone's personal profile information.](myprofile.PNG)

![A view showing a list of Homes, ordered by distance, away from an Organization's center.](homelist.PNG)

--------------------------------------------------------------------------------

# Sketches

## Organization views

### What does the Org need?

#### Org Needs List view
![An Org's view of items that they require. They can mark specific groups as high, mid, or low priority, and exclude entire item groups for specific reasons.](org_needs_view.jpg)

### What are people donating?

#### Org Donators List view
![An Org's view of donators and what they have to donate in a list sorted by distance, ascending.](org_donators_list_view.jpg)

#### Org Donators Map view
![An Org's view of a map with donators as little dots within a 1-mile radius, as well as what they have to donate. ](org_donators_map_view.jpg)

--------------------------------------------------------------------------------
## Driver views

### Whilst driving 1
![App view of a van driver's map with their route intersecting people who wish to donate goods to the shelter.](driver_view_1.jpg)

--------------------------------------------------------------------------------
## Donator views

### Donator Inventory View
![A Donator's view of their current inventory. They have groups and subgroups like Food and Perishables, and can collapse and expand any group. They enter inventory as a number for each item, like `(3) Canteloupe`](donator_inventory_view.jpg)

--------------------------------------------------------------------------------
## ER Diagrams

### User-House-Items relationship  
![An Entity-Relationship Diagram that details how Users should have one or more Houses and houses have a single list of Items](erdiagram.PNG)

--------------------------------------------------------------------------------
## Miscellaneous views

### Data JSON to HTML element

#### What we need it to look like
![A diagram showing our tree representation of a list of items and its human-friendly form equivalent, side-by-side.](dict_to_html.jpg)

#### Recusive implementation
![A diagram explaining how, through recursion, one would convert an N-ary tree of any amount of groups and subgroups into its HTML equivalent.](dict_to_html_2.jpg)
