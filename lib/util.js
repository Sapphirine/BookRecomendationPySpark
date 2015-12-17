var Book = React.createClass({
	render: function() {
		return (
  				<div className="col-sm-6 col-md-4">
    				<div className="thumbnail">
      					<img style={imageShadowStyle} src={this.props.book[4]} alt={this.props.book[0]}/>
      					<div className="caption">
        					<h3>{this.props.book[0]}</h3>
    			    		<p>Author: {this.props.book[2]}</p>
							<p>Publisher: {this.props.book[3]}</p>
        					<div>
        						<div className="ratings" id={this.props.book[6]}>
        						</div>
        					</div>
  				    	</div>
  				  	</div>
  				</div>
		);
	},
});

var imageShadowStyle = {
  width:"180px",
  height:"320px"
};

var BookList = React.createClass({
	getInitialState: function() {
	    return {loading: true};
	},
	render: function() {
		if (this.state.loading) {
			return (
					<div className="ui segment">
  						<div className="ui active inverted dimmer">
    					<div className="ui text loader">Loading</div>
  						</div>
  						<p></p>
					</div>
				);
	    }
		
	    return (
	       <div className="row">
	    	{
	    		this.state.data.map(function(book) {
	    			return <Book key={book[6]} book={book}/>
	    		})
	    	}
	       </div>
	    );
	},
	
     componentDidMount : function() {
    	 $.get("getRecommendation", function(result) {
    		 this.setState(
    			{
    				loading: false,
    				data: JSON.parse(result)
    			}
    		);
        }.bind(this));
	 },
	 componentDidUpdate : function() {
		$('.ratings').raty({	number: 10 ,
 	 						 	click: function(score, evt) {
    								$.post("rate",{ bookid: this.id, score: score });
  							 	}
							});
	 },
});

ReactDOM.render(
		<BookList/>,
		document.getElementById('recommendList')
	);