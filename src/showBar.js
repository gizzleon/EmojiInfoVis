/*--------------------------------------------- SHOW BAR CHARTS INTERACTIVELY WITH THE MAP -------------------------------*/
function showBar(a){
		switch(a){
		        case 1:
			    drawBar(geo_data.AL);
				break;
			    case 2:
			    drawBar(geo_data.AK);
				break;
			    case 3:
			    drawBar(geo_data.AZ);
				break;
                case 4:
			    drawBar(geo_data.AR);
				break;
			    case 5:
			    drawBar(geo_data.CA);
				break;
			    case 6:
			    drawBar(geo_data.CO);
				break;
			    case 7:
			    drawBar(geo_data.CT);
				break;
			    case 8:
			    drawBar(geo_data.DE);
				break;
				case 9:
				drawBar(geo_data.DC);
				break;
			    case 10:
			    drawBar(geo_data.FL);
				break;
			    case 11:
			    drawBar(geo_data.GA);
				break;
			    case 12:
			    drawBar(geo_data.HI);
				break;
			    case 13:
			    drawBar(geo_data.ID);
				break;
			    case 14:
			    drawBar(geo_data.IL);
				break;
			    case 15:
			    drawBar(geo_data.IN);
				break;
			    case 16:
			    drawBar(geo_data.IA);
				break;
			    case 17:
                drawBar(geo_data.KS);
				break;
				case 18:
                drawBar(geo_data.KY);
				break;
				case 19:
                drawBar(geo_data.LA);
				break;
				case 20:
                drawBar(geo_data.ME);
				break;
				case 21:
                drawBar(geo_data.MD);
				break;
				case 22:
                drawBar(geo_data.MA);
				break;
				case 23:
                drawBar(geo_data.MI);
				break;
				case 24:
                drawBar(geo_data.MN);
				break;
				case 25:
                drawBar(geo_data.MS);
				break;
				case 26:
                drawBar(geo_data.MO);
				break;
				// case 27:
                // drawBar(geo_data.MT);  // no data for MT
				// break;
				case 28:
                drawBar(geo_data.NE);
				break;
				case 29:
                drawBar(geo_data.NV);
				break;
				case 30:
                drawBar(geo_data.NH);
				break;
				case 31:
                drawBar(geo_data.NJ);
				break;
				case 32:
                drawBar(geo_data.NM);
				break;
				case 33:
                drawBar(geo_data.NY);
				break;
				case 34:
                drawBar(geo_data.NC);
				break;
				case 35:
                drawBar(geo_data.ND);
				break;
				case 36:
                drawBar(geo_data.OH);
				break;
				case 37:
                drawBar(geo_data.OK);
				break;
				case 38:
                drawBar(geo_data.OR);
				break;
				case 39:
                drawBar(geo_data.PA);
				break;
				case 40:
                drawBar(geo_data.RI);
				break;
				case 41:
                drawBar(geo_data.SC);
				break;
				case 42:
                drawBar(geo_data.SD);
				break;
				case 43:
                drawBar(geo_data.TN);
				break;
				case 44:
                drawBar(geo_data.TX);
				break;
				case 45:
                drawBar(geo_data.UT);
				break;
				case 46:
                drawBar(VT);        
				break;            
				case 47:
                drawBar(geo_data.VA);
				break;
				case 48:
                drawBar(geo_data.WA);
				break;
				case 49:
                drawBar(geo_data.WV);
				break;
				case 50:
                drawBar(geo_data.WI);
				break;
				case 51:
                drawBar(geo_data.WY);
				break;
				case 52:
                drawBar(geo_data.co); //PR
				break;	
                default: ;				
		} ;
		if(a==0){svg.selectAll(".bar").remove();   //This is for the purpose of removing previous bar chart before showing a new one
		         svg.selectAll("g").remove();};
		};