import React,  { memo } from "react";
import {
  ComposableMap,
  Geographies,
  Geography,
  ZoomableGroup
} from "react-simple-maps";

import { scaleLinear } from "d3-scale";


const geoUrl =
  "https://raw.githubusercontent.com/zcreativelabs/react-simple-maps/master/topojson-maps/world-110m.json";

const colorScale = scaleLinear()
  .domain([50, 100])
  .range(["#ff0000", "#4fff5b"]);

const MapChart = (props) => {
  return (
    <ComposableMap
      projection="geoAlbers"
      projectionConfig={{
        rotate: [-40, -15, 15],
        scale: 450
      }}
      height={440}
      data-tip=""
    >
        {console.log(props)}
        <ZoomableGroup zoom={1}>
      {(
        <Geographies geography={geoUrl}>
          {({ geographies }) =>
            geographies.map((geo) => {
            let d = false;
            if (geo.properties.ISO_A3 in props.data){
                d = props.data[geo.properties.ISO_A3];
            }
            return (
                <Geography
                key={geo.rsmKey}
                geography={geo}
                fill={d ? colorScale(d["Overall"]) : "#dedede"}
                onMouseEnter={() => {
                  if(d){
                    d["Country"] = geo.properties["NAME"];
                    props.setTooltipContent(d)
                  }
                  else{
                    props.setTooltipContent(false)
                  }
                }}
                onMouseLeave={() => {
                    props.setTooltipContent("");
                }}

                style={{
                    hover: {
                      fill: "#18A8D8",
                      outline: "none"
                    },
                    pressed: {
                      outline: "none"
                    }
                  }}

                />
            )
            })
          }
        </Geographies>
      )}
      </ZoomableGroup>
    </ComposableMap>
  );
};

export default memo(MapChart);