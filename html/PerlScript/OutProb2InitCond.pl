#!/usr/bin/perl -w
# Example of command:  | xargs -0 ./OutProb2InitCond.pl
# Carefull in the command: . must be replaced by \.
use strict;
use List::MoreUtils qw(uniq);
$_=shift;
my @LineList=split(/\t/);
my @NodeList;
foreach (@LineList)
{if (/[A-Z,a-z]/ & !/<nil>/) {@NodeList=(@NodeList,split(/ -- /));}}
@NodeList=uniq(@NodeList);
my $LineInitCond="[".$NodeList[0];
foreach (@NodeList[1..$#NodeList])
{$LineInitCond=$LineInitCond.",".$_;}
$LineInitCond=$LineInitCond."].istate =";
for (my $index=0;$index<=$#LineList;$index++) 
{
    $_=$LineList[$index];  
    if (/[A-Z,a-z]/) 
    {
	$LineInitCond=$LineInitCond.$LineList[$index+1]." [";
	if (/$NodeList[0]/) {$LineInitCond=$LineInitCond."1";}
	else {$LineInitCond=$LineInitCond."0";}
	foreach my $Node (@NodeList[1..$#NodeList])
	{
	 $LineInitCond=$LineInitCond.",";
	 if (/$Node/) {$LineInitCond=$LineInitCond."1";}
	else {$LineInitCond=$LineInitCond."0";}
	}
	$LineInitCond=$LineInitCond."] , ";	
    }
}
chop($LineInitCond);
chop($LineInitCond);
$LineInitCond=$LineInitCond.";\n";
printf $LineInitCond;
