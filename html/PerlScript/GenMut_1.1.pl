#!/usr/bin/perl -w
use strict;

my $MaxRate="1.7976931348623157E+308";
my $MaBossScript="PlMaBoSS_2.0.pl"; #script that run MaBoSS
my $bnd_file=shift;
#Error test (produce a "help")
if (!$bnd_file){
    printf "Missing bnd file, GenPertCfg.pl  <file.bnd> \"<node_list>\"\n"; 
    exit;}

my $n_list=shift;
if (!$n_list){
    printf "Missing string to add, GenMut.pl  <file.bnd> \"<node_list>\"\n";
    exit;}

my @node_list=split(/\s+/,$n_list);

#$_=$cfg_file;
#s/.cfg//;
#my $cfg_name=$_; #not use yet, new version may generates multiple cfg files
open(BND_F,$bnd_file) || die "Cannot find bnd file ".$bnd_file."\n";
my @MutBNDLineList;
do
{
    $_=<BND_F>;
    @MutBNDLineList=(@MutBNDLineList,$_);
    until((/node/ || eof(BND_F))) {$_=<BND_F>;@MutBNDLineList=(@MutBNDLineList,$_);} #catch line starting with "node" 
    if(!eof(BND_F))
    {
	foreach my $node (@node_list) #catch if node name correspond a name in the list of nodes
	{
	    if(/$node/)
	    {
		print "Catch node ".$node."\n";
		my $rate_up_flag=0;
		my $rate_down_flag=0;
		do {
		    $_=<BND_F>;
		    if(/rate_up/)
		    {
			my $up_var=" = ( \$Low_".$node." ? 0.0 : ( \$High_".$node." ? \@max_rate : ("; #Low_node wins
			s/=/$up_var/;
			s/;/)));/;
			@MutBNDLineList=(@MutBNDLineList,$_); #change the rate_up
			$rate_up_flag=1;	
		    }
		    elsif(/rate_down/)
		    {
			my $down_var=" = ( \$Low_".$node." ? \@max_rate : ( \$High_".$node." ? 0.0 : (";#Low_node wins
			s/=/$down_var/;
			s/;/)));/;
			@MutBNDLineList=(@MutBNDLineList,$_); #change the rate_down
			$rate_down_flag=1;
		    }
		    else{@MutBNDLineList=(@MutBNDLineList,$_);}
		}
		until(/\}/);
		if ($rate_up_flag==0)
		{
		    splice(@MutBNDLineList,$#MutBNDLineList-1,0,"\t rate_up = ( \$Low_".$node." ? 0.0 : ( \$High_".$node." ? \@max_rate : (\@logic ? 1.0 : 0.0 )));\n");
		    #if rate_up is absent, create it. Low_node wins
		}
		if ($rate_down_flag==0)
		{
		     splice(@MutBNDLineList,$#MutBNDLineList-1,0,"\t rate_down = ( \$Low_".$node." ? \@max_rate : ( \$High_".$node." ? 0.0 : (\@logic ? 0.0 : 1.0 ))) ;\n");
		     #if rate_down is absent, create it. Low_node wins
		}
		splice(@MutBNDLineList,$#MutBNDLineList,0,"\t max_rate = ".$MaxRate.";\n"); #local definition of Max_rate
		last; #if a node is catched, no need to further run the foreach loop
	    }
	}
    }
}
until(eof(BND_F));
close(BND_F);
$_=$bnd_file;
s/\./_mut\./;
open(BND_F_MUT,">".$_);
foreach my $line (@MutBNDLineList)
{print BND_F_MUT $line;}
close(BND_F_MUT);
