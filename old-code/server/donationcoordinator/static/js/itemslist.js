
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
    toggleClass(p, 'hidden');
}

function removeAllClasses(c)
{
    $('.'+c).each(function(i, elt) {
        $(this).removeClass(c);
    });
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

$(document).on('keyup', function(e) {
    if(e.keyCode == 27)
    {
        removeAllClasses('hidden');
        removeAllClasses('highlighted');
        $('#items-search input').val('');
    }
});

$('#items-search input').on('keyup', function(e) {
    var val = $(this).val();

    val = val.replace(' ','_');

    if(val == "")
    {
        removeAllClasses('hidden');
        removeAllClasses('highlighted');
        return;
    }

    //show all as we will assume that all have what we are seeking
    $('form li').each(function(i, elt) {
        $(elt).addClass('hidden');
    });

    var s = 'li[class*='+val+']';

    print("Selector: ");
    print(s);

    $(s).each(function (i, elt) {
        print("match:");
        print(this);

        $(this).removeClass('hidden'); //shows elt we want

        e = this.parentElement
        while(e.nodeName !== "FORM") //bubble up repeatedly
        {
            $(e).removeClass('hidden');
            $(e).addClass('highlighted');
            e = e.parentElement;
        }

    });

});

});