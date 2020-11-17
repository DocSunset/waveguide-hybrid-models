2020-11-16

So I'm trying to hybridize the cane reed excitation model seen in the STK
clarinet and saxophony models with the STK bowed and STK flute excitation
models. 

The cane model has offset (b) and slope (m) parameters; 

y = mx + b
clipping implicit

these principally may be thought of as shifting the line graph up or down, and
changing the slope respectively.  However, due to the presence of the clipping
nonlinearity, the offset almost acts more like a left-right shift.  Similarly,
the slope could equally be considered as a stretching along the x-axis.

Viewing the slope and offset in this way, we can apply stretching and shift
to the flute nonlinearity pretty readily.  I've been using the nonlinearity

y = ax^3 + (1 - a)x

with -0.5 <= a <= 4.  This is nice because it gives very immediate control over
what I would describe as the "amount of distortion" in a very satisfying way by
varying the `a` parameter.  This mapping happens to always map to the range 
between -1 and 1.

With stretching and shifting along the x axis we get this:

y = a(mx + b)^3 + (1 - a)(mx + b)

This is very clearly the composition of the first and second functions, which
would go on to be composed with the clipping function:

x -> (reed) -> (flute labium) -> (clipping) -> y

Crucially, when a = 0, this composition reduces to the first function, which
implies a way that we could turn off the flute-inspired influence in the model.

---

There is a bit of a hitch though. In the flute model, the full nonlinear
excitation section has this form:

x = breath + negated reflection
y = clip( x^3 - x )

In contrast, the clarinet looks like this:

x = negated reflection - breath
y = clip( x * (mx + b) + breath )

So there are some extra terms in there, and it's a bit unclear how to reconcile
them.  The difference in the definition of x appears like it may be a major
issue, but in fact the flute model performs equally well if you use the
clarinet's version where the breath signal is negated.

Lets rewrite the flute equations:

x = reflection - breath
y = clip( x * (x^2 - 1) )

This implies that the version of the flute nonlinearity described above, with
the a term for tuning the distortion, may not be as useful as thought. And
indeed, more playing with the flute model including this modification does show
it to be a bit eccentric in places; forget I ever mentioned it.

So now we have the flute and clarinet equations looking like this (let the 
reflection = r, breath = h)

x = r - h
flute = clip( x * (x^2 - 1) )
clari = clip( x * (mx  + b) + h )

So lets mash them together with a simple first stab:

flarinette, flurette, fluri, clute, clarute, clarinute
y = clip ( x * (m * x^p + b) + qh )

Playing with this it strikes me how little effect the qh term appears to have
looking at a graph. Does the clarinette still work without that?

Yes, yes it does. HOWEVER! Although it still makes sound, the playable range
of breath pressures is severely compressed! What if I go the other way and
double the influence of this term? Or how about adding it to the flute model?

Increasing the influence of this term does indeed make the model a bit more
responsive. However, it also makes it easier to blow up...

Adding the qh term to the flute is a bit curious. The model still sounds, but
its playable breath pressure range is a bit strangely effected; it saturates
more easily causing the model to become silent. It more or less works though?

Interestingly, with the qh term removed from the flute model, it starts to
speak around the same breath pressure as the flute model...

The x^p term is not going to work; the fractional powers appear not to be
defined for inputs less than or equal to zero. Need to find a better approach
to move between the two for this term...  Maybe a simple crossfade?

y = clip ( x * (pmx + (1-p)mx^2 + b) + qh )

Alternatively, could we rewrite the clarinet equation to simplify it a bit?

y = clip ( mx^2 + bx + qh )

Aha! The similarities grow greater and greater... This suggests a hybrid of
this form:

y = clip ( ax^3 + cx^2 + bx + qh )

Now I'm getting into whirlwind territory. The question now becomes, what are
the criteria for this polynomial to make sound?
