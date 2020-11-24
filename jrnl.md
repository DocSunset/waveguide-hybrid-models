2020-11-17

Where we left off, we had considered the mathematical similarities in the
excitation mechanisms of the flute and clarinet models. I have just implemented
an excitation model of the following form:

y = clip ( x * (smx + (1-s)mx^2 + b) + qh )

which I have implemented as:

`let y = d * ( s*m*d + (1-s)*m*d*d + b) + q*h;`

With m = -0.8, b = 0.6, q = -1, s = 0 we get the stk clarinet
With m = 1, b = -1, q = 0, s = 1 we get something like the stk flute

In between we get an unstable silent mess. Sometimes the system blows up
suddenly. Most of the time it is just silent. I am going to have to try a
different approach.

My next test will be to have both excitation models running simultaneously and
crossfade between their outputs. I reason that as long as the amplitude effect
of the different models is in phase (it may be necessary to delay one of the
excitation sections by a wavelength) then they may be able to coexist.

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

2020-11-18

So the model will be something like the following. All of the phase altering
coefficients (the reflection, whether the breath has to be subtracted or added
to the reflection, etc.) are collected into the nonlinearities.

```soul
let xc = -0.95 * r - h; 
let xf = -0.5  * r + h;
let c = xc * ( m * xc + b) + h; 
let f = xf * (xf * xf - 1); // could add a scaling term to xf for distortion gain...
let y = clip(F * f + C * c);
```

Further excitation models may be added with their own mixing coefficients (C
and F above).  Again, it may be necessary to seperate the excitations in order
to delay some by a half wavelength to a full wavelength, although these
adjustments may be possible to achieve by tweaking the math a bit as well.

---

This went very well. The excitation models work well together or alone. There
is lots of room for improvement in the mapping from the sliders to the actual
parameter values, but there you go. It seems to work nicely. Lets try adding
the flute jet delay.

Yes, that also works marvelously; it's particularly intersting to explore how
the jet delay interacts with the clarinet model!

Lets go further: I would like to add the "tone hole" simulation from the '92
clarinet model, a second waveguide branch for simulating excitation position
along the string, karplus-strong style string excitations with comb filtering
and character filtering, a bowing excitation model, and the '92 lip excitation
model.

For starts though, lets just add the clarinet tone hole.

2020-11-19

Today we add the trumpet excitation. That would bring the model up to parity
with the whirlwind, at least in terms of excitation. 

I'm having no luck at all getting the hose player model to work. I've tried
twice now to very meticulously copy the STK implementation, but to no avail.

2020-11-21

Now that the bowed string is working, and given the time left until the
deadline, I think the natural next step is to start consolidating the main
thrust of the work I've done; clean up and final hybrids.

Here's the todo list:
[x] flute
[x] blotar
[x] clarinet
[x] clarinute
[x] bowed
[x] saxofony
[x] saxobowy

If theres time after thats all ready for presentation, then I will add the
blotar into the mix with the saxobowy

2020-11-22

There are a number of ways that you could go about combining multiple excitation
methods simultaneously. With the current clarinot implementation, I am mixing
the outputs of both excitation models and feeding them the same inputs from
both the waveguide and the energy source (breath pressure). This seems to work
alright, but there are definitely some issues; in particular, when both
excitation methods are turned all the way up it leads to pretty severe clipping.

What if instead I adjust the amount of energy only, while taking both outputs
simultaneously? In short, this doesn't work at all. The model is unstable and
immediately blows up as soon as energy is put into the system; I guess this
is because, even if one of the excitation models isn't receiving any energy,
it still gets the state from the rest of the system. Having both outputs
without any attenuation then causes everything to blow up.

One tricky detail in combining the saxofony and bowed models is that the saxo
model has a lot of DC offset on its waveguides that causes the bowed model
to become unstable. Fortunately, the bowed model doesn't seem perturbed by 
having a DC blocker in its loop.

It seems to matter more which of the excitation models receives/outputs more
energy from the system rather than which one receives greater energy input.
In general, the bow model appears to dominate the reed model, and it doesn't
seem possible to make them cooperate harmoniously. I wonder if there is a phase
mismatch...

2020-11-23

So I've been thinking about the way that these physical models work on a purely
mathematical level. Throw out all of the physical intepretation of the models
and just consider them as non-linear maps from x[n] to x[n+1]. What is it about
these models that allows them to make sound? What are the minimum conditions
needed for any model to produce sound?

The case of the clarinet is particularly simple, because it can be reduced to
just a non-linearity attached to a waveguide. The non-linearity happens to be a
quadratic function with clipping, with some shifting and scaling so that the
part of the quadratic map where you get the oscillations happens to lie in the
plus and minus one region that we like to work with for audio. 

The only necessary requirement to make a map oscillate is that the slope near
the intersection of the line y = x has to be less than -1, and there has to be
something to keep the value from just diverging to infinity. A line with
clipping is enough to do that, and using this as the non-linearity coupled to
the waveguide also succeeds in producing a square wave. In this model you can
activate oscillation by turning the slope down past -1; I call it the
squarinette(1).

Unfortunately, there isn't much expressive control of the oscillations. They
just snap on as soon as the slope passes the value where there is a bifurcation
in the topology of the map. The clarinet has the nice property that the
amplitude of its orbit gets bigger as the breath pressure gets pushed up, which
translates into a nice amplitude (and also interestingly brightness) increase
as the breath pressure goes up.  This property is also seen in the logistic
map; as the parameter of the logistic map increases, the amplitude of its
(at times strange) orbit grows as well.

This leads me to wonder if a productive instrument could be produced using the
logistic map as a starting point.  The map itself isn't amenable to being
scaled or shifted around, but this could be done at the output.

This actually works quite nicely, with just a few additional considerations:
 - the input to the logistic map has to be clamped to make sure the model can't
   blow up, since the map diverges with negative inputs or those greater than 1
 - the output reqires a DC blocker to remove the DC offset inherent in the map

The resulting instrument is quite interesting, especially along with
interesting delay line structures inspired by real instruments such as the
filter and the 1992 extra-delay-line tone hole model.
