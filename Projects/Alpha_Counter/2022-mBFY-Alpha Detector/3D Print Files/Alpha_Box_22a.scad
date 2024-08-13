/*
 * Alpha_Box_22a based on Half_Breadboard_Rnd_22a
 * ProfHuster@gmail.com
 * 2021-04-12
 *
 * This is case that holds a half breadboard
 * Room for LEGO to mount and space an alpha source
 * 
 * v21a - Initial build
 * v21b - Add lid
 * v21c - Parameterized snaps in lid
 *        Breadboard is "upsidedown"
 * v22a - Making 1/2 breadboard project box
 */
include <screws.scad>
include <RoundedBottomBox_21f.scad>

eps = 0.1;
eps2 = 2 * eps;
$fn=24;

printBase = true;
flipLid = true;
printLid = true;
printHBB = false;
printLEGO = false;

// BREADBOARD PARAMETERS
// Half Breadboard
boardL = 83;
boardW = 56;
boardH = 9.5;
// Model tabs as square of 2x2x6 mm
tabL = 2;
tabH = 6;

// Positions of tabs on BB
tabX = [56, 56, 4, 50]; 
tabY = [14, 68, 83, 83];

module halfBB(){
    color("pink"){
        cube([boardW, boardL,, boardH]);
        for(i = [0:len(tabX)-1]){
            echo(i);
            translate([tabX[i], tabY[i], 0])
                cube([tabL, tabL, tabH]);
        }
    }
}

// CASE PARAMETERS
caseTh = 2.5;
caseR = 3;
caseAngle = 30;
caseClrX = 3; // clearance around board for snaps
electClr = 10; // Height of electronics above bb

caseX = boardW + tabL + 2*caseClrX + 2*caseTh;
caseY = boardL + tabL + 1*caseClrX + 2*caseTh + 80; // snap only in back
caseZ = boardH + caseTh;
lidZ = 18;

// Blocks to position breadboad
lBl = 10;
hBl = 2;
wBl = [3.5,3.5,3.5,3.5,3.0,3.0];
xBl = [caseTh, caseTh, caseX-caseTh-wBl[2], caseX-caseTh-wBl[3], 
        (caseX-caseTh-wBl[4])/2-10, (caseX-caseTh-wBl[4])/2+25];
yBl = [caseTh, 86-lBl , caseTh, 86-lBl, 86+1, 86+1];
zBl = caseTh;
thBl = [0, 0, 0, 0, 90, 90];

// Lid Stuff
// Snap parameters
// Stick up tabs with snap ridges
// X,Y,L,lidZ,R,TH,Angle
srX0 = [0, 0, caseX, caseX];
srY0 = [20+caseTh+0.5, caseY-caseTh-0.5, 
           caseTh+0.5, caseY-caseTh-20-0.5];
srL0 = [20, 20, 20, 20];
srAngX0 = [0, 0, 0, 0];
srAngY0 = [180, 180, 180, 180];
srAngZ0 = [180, 180, 0, 0];
srParams0 = [srX0, srY0, srL0, srAngX0, srAngY0, srAngZ0];

// Lid Vents
hh=15;
RPventLX = [caseX/2-10]; // USB for breadboard
RPventLY = [0];
RPventLZ = [lidZ-hh+eps];
RPventLW = [20];
RPventLH = [hh];
RPventLL = [2*caseTh];
RPventLAng = [0];


// Bottom
module BBRndCase(){
  union(){
    difference(){
      color("lightblue")
      RoundedBottom(caseX,caseY,caseZ,caseR,
        caseTh,caseAngle);
    }
    // Add positioning block for BB
    for(i=[0:len(xBl)-1]){
        color("lavender")
            translate([xBl[i],yBl[i],zBl])
            rotate([0,0,thBl[i]])
            cube([wBl[i],lBl,hBl]);
        
    }
  }
}

module RPiRndLid(){
  union(){
    difference(){
      color("wheat") 
      RoundedLid(caseX,caseY,lidZ,caseR,
          caseTh,caseAngle, srParams0);
      // Access holes (I call "vents")
      for(i = [0:len(RPventLX)-1]){
        translate([RPventLX[i],
          RPventLY[i]-eps, 
          RPventLZ[i]])
          rotate([0,0,RPventLAng[i]])
          color("yellow")
          cube([RPventLW[i],RPventLL[i],RPventLH[i]]);
      }
    }
  }
}



if(printBase){
  BBRndCase();
}

if(printHBB){
    translate([caseTh+caseClrX+1,caseTh+0.5,caseTh])
        halfBB();
}


if(printLid){
  if(flipLid){
    translate([-caseX-5,0,0])
      RPiRndLid();
  } else {
    translate([caseX,0,caseZ+lidZ+4])
      rotate([0,180,0])
      RPiRndLid();
  }
}

if(printLEGO){
    translate([caseX/2-8,boardL+caseTh+5*3.2,,0])
        cube([2*8,6*8,9.6]);
}

// EOF