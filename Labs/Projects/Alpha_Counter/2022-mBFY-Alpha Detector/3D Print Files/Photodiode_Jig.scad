/*
 */
include <screws.scad>
include <RoundedBottomBox_21f.scad>

eps = 0.1;
eps2 = 2 * eps;
$fn=48;

W = 80;
L = 20;
H = 20;
x1 = 3;
d1 = 8;

dPD = 8.6;
zPD = H-2.5;

difference(){
    cube([W, L, H]);
    translate([-eps,L/2,zPD])
        rotate([0,90,0])
        cylinder(d=dPD, h = W+eps2);
    translate([3,-eps,H-d1+eps])
        cube([W/2,L+2,d1]);
}

// EOF