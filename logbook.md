# Super Seashells

## 2019 - Initial Work

This repo is an implementation of the [Super Seashells](https://github.com/ptrgags/virtual-museum/blob/master/super_seashells.md)
family of parametric surface I made as part of a project in senior year of college.
This produces seashell surfaces with super-elliptical cross-sections.

The initial code produces a mesh in OBJ format since that is easy to generate.

## 2021-07-15 - GLB Output and Future Directions

Now that I work at Cesium and am a lot more familiar with glTF and GLB formats,
I decided to try generating shells in GLB format. This proved to be simple to
do in Python, as byte strings are easier to operate than JavaScript typed
arrays.

However, I noticed a couple things I should address in the future:

* I'm not following the glTF convention where y is up and z is forward.
* There are no materials or texture coordinates. I have plans for texturing,
    so I hope to do this soon.

### Paper Discovery

I also came across a 1992 paper ["Modeling seashells"](http://algorithmicbotany.org/papers/shells.sig92.pdf)
which did a few things different:

* The generating curve was made from Bezier curves, and not necessarily a
    closed curve.
* The paper uses the [Frenet-Serret formulas](https://en.wikipedia.org/wiki/Frenet%E2%80%93Serret_formulas)
    to compute the curve in steps of constant arc length instead of time. This
    is to give more even spacing between points
* The paper modifies the shell form with sine waves to produce ridges
* The paper uses a specialized reaction-diffusion simulation to model
    the pigmentation patterns of the shells. Recently, [I tried this out](https://github.com/ptrgags/processing-sketchbook/tree/master/SeashellTexture) in
    p5.js, eventually I want to apply that here.

I'm not sure how much of the paper I plan to implement, but I certainly want
to revisit some details here. If so, this will be done separately from the
superseashells formula.

### New Direction

Given the paper mentioned above and other things I've learned about generative
art and differential equations, I want to design a new model of abstract-looking
seashells combining these ideas:

1. A seashell shape is a cross section extruded along a curved path. Parametric
    curves like a helical spiral can be derived directly, but you could also
    define them in terms of curvature. By integrating the [Frenet-Serret formulas](https://en.wikipedia.org/wiki/Frenet%E2%80%93Serret_formulas)
    this can be generalized to _any_ 3D curve. See 
    _Differential Geometry of Curves and Surfaces_ by do Carmo. Also, a 2014
    Bridges paper["Taking a Point for a Walk"](https://archive.bridgesmathart.org/2014/bridges2014-337.pdf)
    about self-avoiding random walks seems relevant.
2. I recently learned about differential growth from a few articles: [Floraform](https://n-e-r-v-o-u-s.com/blog/?p=6721), 
    [this Medium article by Jason Webb](https://medium.com/@jason.webb/2d-differential-growth-in-js-1843fd51b0ce)
    and [this article series from Inconvergent](https://inconvergent.net/generative/differential-line/)
    It would be cool if the cross-section involved some form of differential growth
3. The Seashell ["Modeling seashells"](http://algorithmicbotany.org/papers/shells.sig92.pdf)
    describes 2 systems of differential equations for modeling the pigmentation
    patterns as a reaction-diffusion system. I want to try generalizing these
    equations in some or all of the following ways:
    * Use a variable number of chemicals, though in practice I'll probably use
        2-4 given that most image formats are limited to 4 channels
    * Create more symmetry in the equations, with plenty of parameters to
        control the amounts of each term. For example, every equation would
        get a fill rate and a kill rate, even if they're 0
    * Allow experimenting with different chemical reactions. Typical reaction
        diffusion amounts to a reaction like `A + 2B -> 3B` (see the
        [Reaction-Diffusion Tutorial](https://www.karlsims.com/rd.html) by
        Karl Sims for example). But there's so many more possibilities here,
        perhaps different ratios like `2A + 3B -> 5A` or include some sort of
        oscillatory behavior between multiple chemicals:  `A + B -> C`, 
        `B + C -> A`, `C + A -> B`. There's plenty to try here.
    * Experiment with other differential equation terms. For example, maybe try
        [advection](https://en.wikipedia.org/wiki/Advection) according to a
        velocity field? Or just put various functions (trig functions,
        polynomials, etc) in the equation until I
        find something interesting. Since I'm just simulating the differential
        equations, not solving them analytically, the sky's the limit
    * Experiment with various initial conditions
    * Experiment with different rules for controlling pigmentation
4. At least for GLB output, experiment with PBR materials. [glTF supports
    metallic-roughness](https://github.com/KhronosGroup/glTF/tree/master/specification/2.0#materials) and there are several [extensions](https://github.com/KhronosGroup/glTF/tree/master/extensions/2.0/Khronos) for other
    types of materials (transparent, sheen, transmission, etc).

This is a lot of details, and plenty I need to learn to do this effectively. I
plan to start by making p5.js sketches to experiment with some of the above.
Those will appear in my other repo, [`processing-sketchbook`](https://github.com/ptrgags/processing-sketchbook)

### Next Steps

1. Add a README for this repo. Include screenshots!
2. Add a revised version of the [Super Seashells](https://github.com/ptrgags/virtual-museum/blob/master/super_seashells.md) description. Include diagrms this time!
3. Fix the y-up issue.
4. Prototype the various parts before combining them in this repo. This could
    take a while.