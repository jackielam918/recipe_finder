import React from 'react';
import { Graph } from "react-d3-graph";
import * as d3 from 'd3'

// the graph configuration, you only need to pass down properties
// that you want to override, otherwise default ones will be used
const easyColor = "#ece7f2";
const mediumColor = "#a6bddb";
const hardColor = "#2b8cbe";


const myConfig = {
    nodeHighlightBehavior: true,
    node: {
        highlightStrokeColor: "blue",
        labelProperty: "recipeName",
        labelPosition: "center",
        strokeWidth: 5
    },
    link: {
        highlightColor: "lightblue",
    },
};

const onClickNode = function(nodeId) {
    window.alert(`Clicked node ${nodeId}`);
};

const onMouseOverNode = function(nodeId) {
    window.alert(`Mouse over node ${nodeId}`);
};

const onMouseOutNode = function(nodeId) {
    window.alert(`Mouse out node ${nodeId}`);
};

class RecipesGraph extends React.Component {
    constructor(props) {
        super(props);
    }

    render(){
        if (this.props && this.props.data && this.props.data.length > 0){
            const data = this.extractNodesAndLinks(this.props.data);
            return <Graph
                id="graph-id" 
                data={data}
                config={myConfig}
                onClickNode={onClickNode}
                onMouseOverNode={onMouseOverNode}
                onMouseOutNode={onMouseOutNode}
            />;
        }
        return <div class="results"></div>;
    }

    //data needs to be like so 
    //const datas = [{
    //     nodes: [{ id: "Harry", size: 300 }, { id: "Sally" }, { id: "Alice" }],
    //     links: [
    //     { source: "Harry", target: "Sally" },
    //     { source: "Harry", target: "Alice" },
    //     ],
    //   }];
    extractNodesAndLinks(datas)
    {
        const nodes = [];
        const tempLinks = [];

        const validLinks = new Set();
        const nodeIds = new Set();

        datas.forEach(data => {
            nodeIds.add(data.id);
            nodes.push(
                    {
                        id: data.id, 
                        recipeName: data.name, 
                        color: data.difficulty === "Easy" ? easyColor : data.difficulty == "Medium" ? mediumColor : hardColor,
                        size: parseInt((data.similarRecipeIds.length * 1000) + 1000 ),
                        strokeColor: d3.interpolateReds(data.numberOfSubstitutions/4.0)
                    });
            data.similarRecipeIds.forEach(simRecipeId => {
                if (validLinks.has(`${data.id}||${simRecipeId}`) || validLinks.has(`${simRecipeId}||${data.id}`)) {
                    return;
                } else {
                    tempLinks.push({ source: data.id, target: simRecipeId },);
                    validLinks.add(`${data.id}||${simRecipeId}`);
                }
                
            });

        });

        const links = [];
        tempLinks.forEach(link => {
            if (nodeIds.has(link.source) && nodeIds.has(link.target))
            {
                links.push(link);
            } 
        });
        
        return {
            nodes: nodes,
            links: links
        };
    }
}



export default RecipesGraph;
