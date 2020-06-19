#!/usr/bin/perl -w
use strict;

#my $MaBossScript="PlMaBoSS_3.0.pl"; #script that run MaBoSS
my $bnd_file=shift;
if (!$bnd_file){
    printf "Missing bnd file, ParamSens.pl  <file.bnd> <file.cfg> \"<add_string>\"  <MaBoSS_script>, the string will be added to every external variable\n"; 
    exit;}
my $cfg_file=shift;
if (!$cfg_file){
    printf "Missing cfg file, ParamSens.pl  <file.bnd> <file.cfg> \"<add_string>\"  <MaBoSS_script>, the string will be added to every external variable\n";
    exit;}
my $mod_string=shift;
if (!$mod_string){
    printf "Missing string to add, ParamSens.pl  <file.bnd> <file.cfg> \"<add_string>\" <MaBoSS_script>, the string will be added to every external variable\n";
    exit;}
$mod_string=$mod_string.";";
my $MaBossScript=shift;
if (!$mod_string){
    printf "Missing string to add, ParamSens.pl  <file.bnd> <file.cfg> \"<add_string>\"  <MaBoSS_script>, the string will be added to every external variable\n";
    exit;}

$_=$cfg_file;
s/.cfg//;
my $cfg_name=$_;

my @CfgLineList;
my @CfgHitLineIndex;
my @CfgVarList;
open(CFG_F,$cfg_file);
my $LineIndex=0;
while(<CFG_F>)
{
    @CfgLineList=(@CfgLineList,$_);
    if (/^\$/)
    {
	s/^\$//;
	@CfgHitLineIndex=(@CfgHitLineIndex,$LineIndex);
	my @LineSplit=split(/=/);
	$_=$LineSplit[0];
	s/\s//g;
	@CfgVarList=(@CfgVarList,$_);
    }

    $LineIndex++;	    
}
close(CFG_F);
open(SRC_F,">script_".$cfg_name.".sh");
for (my $i=0;$i<=$#CfgHitLineIndex;$i++)
{
    my $tmpCfgFile=$cfg_name."_".$CfgVarList[$i].".cfg";
#    print SRC_F $MaBossScript." ".$bnd_file." ".$tmpCfgFile." 0.01\n"; #line that lauch MaBoSS
    print SRC_F $MaBossScript." -c ".$tmpCfgFile." -o Out_".$CfgVarList[$i]." ".$bnd_file."\n"; #line that lauch MaBoSS
    open(CFG_F,">".$tmpCfgFile);
    for ($LineIndex=0;$LineIndex<$CfgHitLineIndex[$i];$LineIndex++)
    {
	print CFG_F $CfgLineList[$LineIndex];
    }
    $_=$CfgLineList[$CfgHitLineIndex[$i]];
    
    s/;/$mod_string/;
    print CFG_F $_;
    
    for ($LineIndex=$CfgHitLineIndex[$i]+1;$LineIndex<=$#CfgLineList;$LineIndex++)
    {
	print CFG_F $CfgLineList[$LineIndex];
    }
    close(CFG_F);
}
close(SRC_F);

	
    

