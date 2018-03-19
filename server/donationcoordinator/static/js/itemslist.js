
$(document).ready(function() //when document loads
{

print = console.log;

function toggleClass(p, c)
{
    if(p.hasClass(c))
    {
        p.removeClass(c);
    }
    else
    {
        p.addClass(c);
    }
}

function toggleView(p)
{
    toggleClass(p, 'hidden')
}

var a_elts = $('section#items form ul a');

print("all <a> elts that will (upon click) collapse their UL elts")
print(a_elts)

a_elts.each(function(i, elt) { //for all <a> tags

    $(elt).on('click', function(event) {

        elem = event.currentTarget.parentElement;
        e = $(elem)

        if(e.hasClass('hidden'))
        {
            e.removeClass('hidden');
        }
        else
        {
            e.addClass('hidden');
        }

    });
});

});